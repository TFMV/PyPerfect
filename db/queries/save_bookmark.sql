-- :name save_bookmark :insert
INSERT INTO bookmarks (bookmark_id, link, org_id, user_id) 
  VALUES (:bookmark_id, :link, :org_id, :user_id); 