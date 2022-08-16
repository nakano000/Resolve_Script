local user_path = app:GetPrefs("Global.Paths.Map.UserPaths:")
if not user_path:find("%$%(RS_FUSION_USER_PATH%)") then
    user_path = user_path .. ";$(RS_FUSION_USER_PATH)"
    app:SetPrefs("Global.Paths.Map.UserPaths:", user_path)
    app:SavePrefs()
end
print("Global.Paths.Map.UserPaths: " .. user_path)
