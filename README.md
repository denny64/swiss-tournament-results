# Tournament Results

** Description **
This project defines the database schema in tournament.sql, and is used it to track a Swiss tournament in tournament.py.
This project is from the (Introduction to Relational Databases)[https://www.udacity.com/course/intro-to-relational-databases--ud197] course from Udacity.

Requirements: 

- Virtual Box
- PSQL
- Python
- Vagrant

To Run:
 
 1. `vagrant up` from inside the vagrant folder (where the vagrant file is)
 2. `vagrant ssh`
 3. `cd /vagrant/tournament`
 4. Run `psql`
 5. `\i tournament.sql` to create the database
 
 To run tests:
 
 - `python tournament_test.py`
 
