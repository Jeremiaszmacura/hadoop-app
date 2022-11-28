/* eslint-disable */
// Create user
db = db.getSiblingDB('test');

db.createUser({  
  user:"user",
  pwd:"user",
  roles:[  
   {  
      role:"readWrite",
      db:"test"
   }
  ],
  mechanisms:[  
   "SCRAM-SHA-1"
  ]
 });

db.createCollection('address_data');

// Authenticate user
db.auth({
  user: "user",
  pwd: "user",
});