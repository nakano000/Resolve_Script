local function AddButton(UseRefresh, UseLoad, UseSave)
    local tool_list = comp:GetToolList(true)
    comp:StartUndo('RS Add Button')
    for i, v in ipairs(tool_list) do
        local uc = v.UserControls
        if UseRefresh then
            uc['Refresh'] = {
                LINKS_Name = 'Refresh',
                LINKID_DataType = 'Number',
                INPID_InputControl = 'ButtonControl',
                INP_Integer = false,
                BTNCS_Execute = "comp:StartUndo('RS Refresh');"
                        .. "local tool_list = comp:GetToolList(false, 'Fuse.RS_GlobalStart');"
                        .. "for k,v in pairs(tool_list) do v:Refresh() end;"
                        .. "comp:EndUndo(true)\n",
                ICS_ControlPage = 'Tools',
            }
        end
        if UseLoad then
            uc['LoadSettings'] = {
                LINKS_Name = 'Load Settings',
                LINKID_DataType = 'Number',
                INPID_InputControl = 'ButtonControl',
                INP_Integer = false,
                BTNCS_Execute = [[
local node = self:GetTool()
local path = fusion:RequestFile(
    '',
    '',
    {
        FReqB_SeqGather = false,
        FReqS_Filter = 'Settings File (*.setting)|*.setting',
        FReqS_Title = 'Load Settings',
    }
)
if path then
    node:LoadSettings(comp:MapPath(path))
    print('Load: ' .. comp:MapPath(path))
end
]],
                ICS_ControlPage = 'Tools',
            }
        end
        if UseSave then
            uc['SaveSettings'] = {
                LINKS_Name = 'Save Settings',
                LINKID_DataType = 'Number',
                INPID_InputControl = 'ButtonControl',
                INP_Integer = false,
                BTNCS_Execute = [[
local node = self:GetTool()
local path = fusion:RequestFile(
    '',
    node.Name .. '.setting',
    {
        FReqB_Saving = true,
        FReqB_SeqGather = false,
        FReqS_Filter = 'Settings File (*.setting)|*.setting',
        FReqS_Title = 'Save Settings',
    }
)
if path then
    node:SaveSettings(comp:MapPath(path))
    print('Save: ' .. comp:MapPath(path))
end
]],
                ICS_ControlPage = 'Tools',
            }
        end
        v.UserControls = uc
        v:Refresh()
    end
    comp:EndUndo(true)
    print('Done!')
end
