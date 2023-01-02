local function getToolName(st)
    for key, v in pairs(st['Tools']) do
        if (type(v) == 'table') and (v['Inputs'] ~= nil) then
            return key
        end
    end
    return nil
end

local function setJimaku(txt, index, setting_path)
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
    local videoItems = timeline:GetItemListInTrack('video', index)
    if #videoItems == 0 then
        print('VideoItemが見付かりません。')
        return
    end
    local textPlus = videoItems[1]

    if textPlus:GetFusionCompCount() == 0 then
        print('FusionCompが見付かりません。')
        return
    end

    local comp = textPlus:GetFusionCompByIndex(1)

    local lst = comp:GetToolList(false, 'TextPlus')
    if not lst[1] then
        print('TextPlus Nodeが見付かりません。')
        return
    end

    local tool = lst[1]

    -- setting
    tool.StyledText = txt
    tool.UseFrameFormatSettings = 0
    tool.Width = tonumber(timeline:GetSetting('timelineResolutionWidth'))
    tool.Height = tonumber(timeline:GetSetting('timelineResolutionHeight'))

    local st = tool:SaveSettings()
    local f_st = bmd.readfile(setting_path)
    if not f_st then
        print(setting_path)
        print('settingファイルの読み込みに失敗しました。')
        return
    end
    local name = getToolName(f_st)
    for i, key in pairs({ 'StyledText', 'UseFrameFormatSettings', 'Width', 'Height' }) do
        f_st['Tools'][name]['Inputs'][key] = st['Tools'][tool.Name]['Inputs'][key]
    end

    -- set
    comp:StartUndo('RS Jimaku')
    comp:Lock()
    tool:LoadSettings(f_st)
    comp:Unlock()
    comp:EndUndo(true)

    print('Dane!(Import Voice, Text+)')
end
