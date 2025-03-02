-- :name delete_bookmark :affected
DELETE FROM bookmarks WHERE bookmark_id = :bookmark_id AND org_id = :org_id; 