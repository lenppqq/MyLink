#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')

c = conn.cursor()

# # Turn on foreign key support
# c.execute("PRAGMA foreign_keys = ON")

# Create users table
c.execute('drop table users')
c.execute('''CREATE TABLE users
	     (email TEXT NOT NULL, 
	      password TEXT NOT NULL,
	      PRIMARY KEY(email))''')

# # Create album table
# # Visibility is 'public' or 'private'
# c.execute('''CREATE TABLE albums
# 	     (name TEXT NOT NULL,
# 	      owner TEXT NOT NULL,
# 	      visibility TEXT NOT NULL,
# 	      FOREIGN KEY (owner) REFERENCES users(email),
# 	      PRIMARY KEY(name, owner))''')

# # Create pictures table
# c.execute('''CREATE TABLE pictures
# 	     (path TEXT NOT NULL,
# 	      album TEXT NOT NULL,
# 	      owner TEXT NOT NULL,
# 	      FOREIGN KEY(album, owner) REFERENCES albums(name, owner),
# 	      FOREIGN KEY(owner) REFERENCES users(email),
# 	      PRIMARY KEY(path))''')

# # Create sessions table
# c.execute('''CREATE TABLE sessions
# 	     (user TEXT NOT NULL,
# 	      session TEXT NOT NULL,
# 	      FOREIGN KEY(user) REFERENCES users(email),
# 	      PRIMARY KEY(session))''')
# c.execute('drop table tempusers')
# c.execute('''CREATE TABLE tempusers
# 	     (email TEXT NOT NULL, 
# 	      password TEXT NOT NULL,
# 	      code TEXT NOT NULL,
# 	      PRIMARY KEY(email))''')

# c.execute('drop table relations')
# c.execute('''CREATE TABLE relations
#          (emaila TEXT NOT NULL, 
#           emailb TEXT NOT NULL,
#           circles TEXT NOT NULL,
#           PRIMARY KEY(emaila, emailb))''')

# c.execute('drop table posts')
# c.execute('''CREATE TABLE posts
#          (email TEXT NOT NULL, 
#           msg TEXT NOT NULL,
#           picture TEXT,
#           time NUMERIC NOT NULL,
#           circles TEXT NOT NULL)''')

# c.execute('drop table circles')
# c.execute('''CREATE TABLE circles
#          (email TEXT NOT NULL, 
#           id INTEGER NOT NULL,
#           name TEXT NOT NULL
#           )''')
c.execute('drop table pi')
c.execute('''CREATE TABLE pi
         (email TEXT NOT NULL, 
          name TEXT NOT NULL,
          picture TEXT NOT NULL
          )''')


# Save the changes
conn.commit()

# Close the connection
conn.close()
