local function set_mb()
    comp.Lock()
    comp:StartUndo('RS Set MotionBlur')
    local tool_list = comp:GetToolList(true)
    for k,v in pairs(tool_list) do
        v.MotionBlur = 1
    end
    comp:EndUndo(true)
    comp.Unlock()
end

set_mb()