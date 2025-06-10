// MongoDB initialization script
db = db.getSiblingDB('fastapi_db');

// Create users collection with indexes
db.createCollection('users');

// Create unique index on email field
db.users.createIndex({ "email": 1 }, { unique: true });

// Create index on name field for faster searches
db.users.createIndex({ "name": 1 });

print('Database initialized successfully!');
