
local function refresh()
    comp:StartUndo('RS Refresh')
    local tool_list = comp:GetToolList(true)
    for k,v in pairs(tool_list) do
        v:Refresh()
    end
    comp:EndUndo(true)
    print('Refresh!')
end

refresh()
