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

local function getTrackIndexByName(timeline, name)
    local r = nil
    local cnt = timeline:GetTrackCount('video')
    if cnt == 0 then
        return r
    end
    for i = 1, cnt do
        if timeline:GetTrackName('video', i) == name then
            r = i
        end
    end
    return r
end

local function getItemByTrackName(timeline, name)
    local r = timeline:GetCurrentVideoItem()
    local index = getTrackIndexByName(timeline, name)
    if not index then
        print('Track not found: ' .. name)
        print('Currentを使います。')
        return r
    end
    local currentFrame = getCurrentFrame(timeline)
    for i, item in ipairs(timeline:GetItemListInTrack('video', index)) do
        if item:GetStart() < currentFrame and item:GetEnd() > currentFrame then
            return item
        end
    end
    print('Item not found: ' .. name)
    print('Currentを使います。')
    return r
end

local function setTatie(color, track_name, parameter_name, setting_path)
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
    local textPlus = getItemByTrackName(timeline, track_name)
    if not textPlus then
        print('VideoItemが見付かりません。')
        return
    end

    if textPlus:GetFusionCompCount() == 0 then
        print('FusionCompが見付かりません。')
        return
    end

    local comp = textPlus:GetFusionCompByIndex(1)
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
    if not tool then
        print('Nodeが見付かりません。')
        return
    end

    -- setting
    local tool_lst = {}
    tool_lst[#tool_lst + 1] = tool
    local attr_filter = {
        ['StyledText'] = true,
        [parameter_name] = true,
    }
    for k, v in pairs(tool:SaveSettings()['Tools'][tool.Name]['Inputs']) do
        if type(v) == 'table' and v['__ctor'] and v['__ctor'] == 'InstanceInput' then
            if attr_filter[v['Source']] then
                local _tool = comp:FindTool(v['SourceOp'])
                tool_lst[#tool_lst + 1] = _tool
            end
        end
    end
    local f_st = bmd.readfile(setting_path)
    if not f_st then
        print('設定ファイルが見付かりません。')
        print(setting_path)
        return
    end
    local keys = f_st['Tools']['MouthAnimBezierSpline']['KeyFrames']
    local new_keys = {}
    local gs = comp:GetAttrs()['COMPN_GlobalStart']
    for i, v in pairs(keys) do
        local rh = v['RH']
        local lh = v['LH']
        if rh then
            rh[1] = rh[1] + gs
        end
        if lh then
            lh[1] = lh[1] + gs
        end
        new_keys[i + gs] = v
    end
    f_st['Tools']['MouthAnimBezierSpline']['KeyFrames'] = new_keys

    -- set
    comp:StartUndo('RS Tatie')
    comp:Lock()
    for i, t in pairs(tool_lst) do
        t:LoadSettings(f_st)
    end
    comp:Unlock()
    comp:EndUndo(true)
    -- color
    if color ~= 'None' then
        textPlus:SetClipColor(color)
    end
    -- end
    print('Dane!(立ち絵)')
end

setTatie(
        '%s',
        '%s',
        '%s',
        [[%s]]
)