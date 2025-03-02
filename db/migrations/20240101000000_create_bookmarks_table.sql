-- migrate:up
CREATE TABLE bookmarks (
  bookmark_id TEXT NOT NULL PRIMARY KEY,
  link TEXT NOT NULL,
  org_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bookmarks_org_id ON bookmarks(org_id);
CREATE INDEX idx_bookmarks_user_id ON bookmarks(user_id);

-- migrate:down
DROP TABLE bookmarks; 