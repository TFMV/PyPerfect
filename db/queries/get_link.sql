-- :name get_link :scalar
SELECT link FROM bookmarks 
  WHERE bookmark_id = :bookmark_id
    AND org_id = :org_id; 