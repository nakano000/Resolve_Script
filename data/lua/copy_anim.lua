local pr_setting = [[
{
	Tools = ordered() {
		PipeRouter1 = PipeRouter {
			CtrlWZoom = false,
			ViewInfo = PipeRouterInfo { Pos = { 338.52, 5.61355 } },
		}
	}
}
]]

local function deepcopy(org)
    local copy
    if type(org) == 'table' then
        copy = {}
        for org_key, org_value in next, org, nil do
            copy[deepcopy(org_key)] = deepcopy(org_value)
        end
        setmetatable(copy, deepcopy(getmetatable(org)))
    else
        copy = org
    end
    return copy
end

local function split(str, ts)
    if ts == nil then
        return {}
    end
    local t = {};
    i = 1
    for s in string.gmatch(str, "([^" .. ts .. "]+)") do
        t[i] = s
        i = i + 1
    end
    return t
end

local function getCurrentFrame(timeline)
    local timecode = timeline:GetCurrentTimecode()
    local fps = tonumber(timeline:GetSetting('timelineFrameRate'))
    local intFps = {
        [23] = 24,
        [29] = 30,
        [47] = 48,
        [59] = 60,
        [95] = 96,
        [119] = 120,
    }
    if intFps[fps] then
        fps = intFps[fps]
    end
    local isDF = false
    if string.find(timecode, ';') ~= nil then
        isDF = true
        timecode = string.gsub(timecode, ';', ':')
    end
    local t = split(timecode, ':')
    local h = tonumber(t[1])
    local m = tonumber(t[2]) + (h * 60)
    local s = tonumber(t[3]) + (m * 60)
    local f = tonumber(t[4]) + (s * fps)
    local drop_frames = 0
    if isDF then
        local _f = fps / 15
        drop_frames = _f * (m - math.floor(m / 10))
    end
    return f - drop_frames
end

local function getItem(timeline, index)
    local currentFrame = getCurrentFrame(timeline)
    local items = timeline:GetItemListInTrack('video', index)
    if not items then
        return
    end
    for i, item in ipairs(timeline:GetItemListInTrack('video', index)) do
        if item:GetStart() <= currentFrame and item:GetEnd() > currentFrame then
            return item
        end
    end
    return nil
end

local function getItems(timeline, index, sf, ef)
    local items = {}
    if not index or index > timeline:GetTrackCount('video') or index < 1 then
        return items
    end
    for i, item in ipairs(timeline:GetItemListInTrack('video', index)) do
        if item:GetStart() < ef and item:GetEnd() > sf then
            items[#items + 1] = item
        end
    end
    return items
end

local function getAnim(comp, tool, sf)
    local lst = {}
    local filter = {
        ['BezierSpline'] = true,
        ['PolyPath'] = true,
        ['XYPath'] = true,
    }

    for k, v in pairs(tool:SaveSettings()['Tools'][tool.Name]['Inputs']) do
        local _tool = tool
        local _attr_name = k
        local _attr = v
        if type(v) == 'table' and v['__ctor'] and v['__ctor'] == 'InstanceInput' then
            _tool = comp:FindTool(v['SourceOp'])
            _attr_name = v['Source']
            _attr = _tool:SaveSettings()['Tools'][_tool.Name]['Inputs'][_attr_name]
        end
        if type(_attr) == 'table' and _attr['__ctor'] and _attr['__ctor'] == 'Input' then
            if _attr['SourceOp'] then
                local _anim = comp:FindTool(_attr['SourceOp'])
                if filter[_anim.ID] then
                    local setting = bmd.readstring(pr_setting)
                    setting['Tools']['PipeRouter1']['Inputs'] = { [_attr_name] = _attr }
                    setting['Tools'][_anim.Name] = _anim:SaveSettings()['Tools'][_anim.Name]

                    local anim_names = {}
                    if _anim.ID == 'BezierSpline' then
                        anim_names[#anim_names + 1] = _anim.Name

                    elseif _anim.ID == 'PolyPath' then
                        -- PolyPath用
                        local _inputs = _anim:SaveSettings()['Tools'][_anim.Name]['Inputs']
                        local attr_list = { 'Displacement' }
                        for i, a in ipairs(attr_list) do
                            if _inputs and _inputs[a] and _inputs[a]['SourceOp'] then
                                local _anim2 = comp:FindTool(_inputs[a]['SourceOp'])
                                if _anim2.ID == 'BezierSpline' then
                                    setting['Tools'][_anim2.Name] = _anim2:SaveSettings()['Tools'][_anim2.Name]
                                    anim_names[#anim_names + 1] = _anim2.Name
                                end
                            end
                        end

                    elseif _anim.ID == 'XYPath' then
                        -- XYPath用
                        local _inputs = _anim:SaveSettings()['Tools'][_anim.Name]['Inputs']
                        local attr_list = { 'X', 'Y' }
                        for i, a in ipairs(attr_list) do
                            if _inputs and _inputs[a] and _inputs[a]['SourceOp'] then
                                local _anim2 = comp:FindTool(_inputs[a]['SourceOp'])
                                if _anim2.ID == 'BezierSpline' then
                                    setting['Tools'][_anim2.Name] = _anim2:SaveSettings()['Tools'][_anim2.Name]
                                    anim_names[#anim_names + 1] = _anim2.Name
                                end
                            end
                        end
                    end

                    -- KeyFrames
                    local gs = comp:GetAttrs()['COMPN_GlobalStart']
                    for i, n in ipairs(anim_names) do
                        local keys = setting['Tools'][n]['KeyFrames']
                        local new_keys = {}
                        for j, v in pairs(keys) do
                            local rh = v['RH']
                            local lh = v['LH']

                            if rh then
                                rh[1] = rh[1] - gs + sf
                            end
                            if lh then
                                lh[1] = lh[1] - gs + sf
                            end
                            new_keys[j - gs + sf] = v
                        end
                        setting['Tools'][n]['KeyFrames'] = new_keys
                    end
                    -- set data
                    lst[#lst + 1] = {
                        tool = _tool.Name,
                        splines = anim_names,
                        st = setting
                    }
                end
            end
        end
    end
    return lst
end

local function getNode(comp)
    local lst = comp:GetToolList(false)
    local tool
    local tool_filter = {
        ['MacroOperator'] = true,
        ['GroupOperator'] = true,
    }
    for i, t in ipairs(lst) do
        if tool_filter[t.ID] and not t.ParentTool then
            tool = t
            break
        end
    end
    return tool
end

local function copyAnim(index)
    local projectManager = resolve:GetProjectManager()
    local project = projectManager:GetCurrentProject()
    if not project then
        print('Projectが見付かりません。')
        return
    end
    local timeline = project:GetCurrentTimeline()
    if not timeline then
        print('Timelineが見付かりません。')
        return
    end

    -- src
    local videoItem = getItem(timeline, index)
    if not videoItem then
        print('VideoItemが見付かりません。')
        return
    end

    if videoItem:GetFusionCompCount() == 0 then
        print('FusionCompが見付かりません。')
        return
    end

    local comp = videoItem:GetFusionCompByIndex(1)
    local tool = getNode(comp)
    if not tool then
        print('Nodeが見付かりません。')
        return
    end
    local anim_lst = getAnim(comp, tool, videoItem:GetStart())

    -- dst
    local dst_items = getItems(timeline, index - 1, videoItem:GetStart(), videoItem:GetEnd())
    for i, item in ipairs(dst_items) do
        if item:GetFusionCompCount() ~= 0 then
            local dst_comp = item:GetFusionCompByIndex(1)
            local sf = item:GetStart()
            local gs = dst_comp:GetAttrs()['COMPN_GlobalStart']
            dst_comp:StartUndo('RS Copy Anim')
            dst_comp:Lock()
            for j, anim in ipairs(anim_lst) do
                local dst_tool = dst_comp:FindTool(anim['tool'])
                -- KeyFrames
                local _setting = deepcopy(anim['st'])
                for k, n in ipairs(anim['splines']) do
                    local keys = _setting['Tools'][n]['KeyFrames']
                    local new_keys = {}
                    for l, v in pairs(keys) do
                        local rh = v['RH']
                        local lh = v['LH']
                        if rh then
                            rh[1] = rh[1] + gs - sf
                        end
                        if lh then
                            lh[1] = lh[1] + gs - sf
                        end
                        new_keys[l + gs - sf] = v
                    end
                    _setting['Tools'][n]['KeyFrames'] = new_keys
                end

                -- apply
                dst_tool:LoadSettings(_setting)
            end
            dst_comp:Unlock()
            dst_comp:EndUndo(true)
        end
    end
end

--copyAnim(3)

