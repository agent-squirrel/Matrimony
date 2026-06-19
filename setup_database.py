#!/usr/bin/env python3
"""
Database setup script for wedding website
Run this script to create the database and tables
"""

import yaml
import pymysql
import sys
import os

# Add current directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_tables():
    """Create all database tables using Flask-SQLAlchemy models"""
    try:
        from app import app, db
        
        print("\nCreating database tables...")
        with app.app_context():
            # Create all tables defined in models
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # List created tables
            inspector_result = db.inspect(db.engine)
            tables = inspector_result.get_table_names()
            print(f"\nTables created:")
            for table in tables:
                print(f"  - {table}")
            
            return True
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def setup_database():
    """Create database and user if they don't exist"""
    
    # Load configuration
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    db_config = config['database']
    
    print("Setting up MariaDB/MySQL database...")
    print(f"Database: {db_config['name']}")
    print(f"User: {db_config['user']}")
    
    # Get root password
    root_password = input("Enter MySQL/MariaDB root password: ")
    
    try:
        # Connect as root
        connection = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user='root',
            password=root_password
        )
        
        cursor = connection.cursor()
        
        # Create database
        print(f"\nCreating database '{db_config['name']}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['name']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Create user and grant privileges
        print(f"Creating user '{db_config['user']}'...")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{db_config['user']}'@'localhost' IDENTIFIED BY '{db_config['password']}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_config['name']}.* TO '{db_config['user']}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Database setup completed successfully!")
        
        # Now create tables
        if create_tables():
            print("\n✅ Full database setup completed!")
            print("\nNext steps:")
            print("1. Run the Flask application: python app.py")
            print("2. Visit http://localhost:5000/admin/setup to create your admin account and configure the wedding")
        else:
            print("\n⚠️  Database created but tables may not have been created. Please check the errors above.")
        
    except pymysql.Error as e:
        print(f"\n❌ Error setting up database: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()
