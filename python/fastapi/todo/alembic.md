What is Alembic?
- Lightweight database migration tool for when using SQLAlchemy
- Migration tools allow us to plan, transfer and upgrade resources within databases
- Alembic allows you to change a SQLAlchemy database table after it has been created
- Currently SQLAlchemy will only create new database tables for us, not enhance any

How does Alembic work?
• Alembic provides the creation and invocation of change management scripts
• This allows you to be able to create migration environments and be able to change data how you like
. Alembic is a powerful migration tool that allows us to modify our database schemes
. It works on tables that already have data. This allows us to be able to continually create additional content that works within our application!
• After we initialize our project with alembic, two new items will appear in our directory
    • alembic.ini
    • alembic directory
• These are created automatically by alembic so we can upgrade, downgrade and keep data integrity of our application

Alembic.ini file
• File that alembic looks for when invoked
• Contains a bunch of configuration information for Alembic that we are able to change to match our project

Alembic Directory
• Has all environmental properties for alembic
• Holds all revisions of your application
• Where you can call the migrations for upgrading
• Where you can call the migrations for downgrading

Alembic Revision?
• Alembic revision is how we create a new alembic file where we can add some type of database upgrade
• When we run:
    • Creates a new file where we can write the upgrade code
    • Each new revision will have a Revision Id

Alembic Upgrade?
• Alembic upgrade is how we actually run the migration
• Enhances our database to now have a new column within our users tables called ‘phone_number’
• Previous data within database does not change

Alembic Downgrade?
• Alembic downgrade is how we revert a migration
• Reverts our database to remove the last migration change.
• Previous data within database does not change unless it was on the column ‘phone_number’ because we deleted it.

Steps:
- Add Connection url string in alembic.ini
- import models in env.py file
- Change target_metadata = models.Base.metadata

Install Command 
- pip install alembic
Setup Command - Initializes a new, generic environment 
- alembic init <folder name>
Create Revision - Creates a new revision of the environment
- alembic revision -m <message>
Upgrade Command - Run our upgrade migration to our database
- alembic upgrade <revision #>
Downgrade Command - Run our downgrade migration to our database
- alembic downgrade -1