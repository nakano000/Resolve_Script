local function marker2Chapter(color, separator)
    print(color .. 'マーカーを目次にします。\n')
    local projectManager = resolve:GetProjectManager()
    local project = projectManager:GetCurrentProject()
    if not project then
        return
    end
    local timeline = project:GetCurrentTimeline()
    if not timeline then
        return
    end
    local fps = timeline:GetSetting('timelineFrameRate')

    local m = timeline:GetMarkers()
    local c = {}
    for i, v in pairs(m) do
        local sec = math.floor(i / fps + 0.5)
        if v.color == color then
            c[#c + 1] = {
                frame = i,
                time = string.format('%02d:%02d', sec / 60, sec % 60),
                name = v.name
            }
        end
    end

    table.sort(c, function(a, b)
        return (a.frame < b.frame)
    end)

    print('目次')
    if c[1] ~= nil and c[1].time ~= '00:00' then
        print('00:00' .. separator)
    end
    for i, v in pairs(c) do
        print(v.time .. separator .. v.name)
    end
end

marker2Chapter('Rose', ' - ')
