local function pathMapper()
    local tool_list = comp:GetToolList(false, 'Loader')
    comp.StartUndo('RS Path Mapper')
    for i, t in ipairs(tool_list) do
        t.Clip[1] = comp:ReverseMapPath(t.Clip[1])
    end
    comp.EndUndo(True)
    print('Mapped!')
end

pathMapper()
