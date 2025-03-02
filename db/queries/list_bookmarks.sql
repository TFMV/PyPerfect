-- :name list_bookmarks :many
SELECT bookmark_id, link, user_id, created_at 
FROM bookmarks 
WHERE org_id = :org_id
ORDER BY created_at DESC; 