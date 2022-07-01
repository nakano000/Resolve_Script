local function printNames()
    local tool_list = comp:GetToolList(true)
    for k,v in pairs(tool_list) do
        print(v.Name)
    end
end

printNames()