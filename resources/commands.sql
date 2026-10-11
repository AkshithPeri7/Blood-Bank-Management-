
-- New Tables
create table if not exists Hospital (HospitalID int(4) primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode int(6) not null)
create table if not exists BloodTable (BloodType char(3), Units int not null, RhFactor char(1))
create table if not exists Recipient (ID int(4) primary key, Name varchar(40), Age int(3), Gender char(20), BloodGroup char(4), Donations int)

-- Tables and their coulmns:
--     Hopsital:  ID, Name, Password, Contact, Pincode
--     BloodTable:  Type, Amount, + or -
--     Recepients:   Name, Age, Gender, Blood Type, donation count, transfusions count
--     Records:   ID, Date, Action

insert into BloodTable values ('A', 0, '+'), ('A', 0, '-'), ('B', 4, '+'), ('B', 0, '-'), ('O', 2, '+'), ('O', 0, '-'), ('AB', 0, '+'), ('AB', 0, '-')
insert into Hospital values (1001, 'Hospital A', 'password', 'hospitalemail@gmail.com / 1233219', 366066)
insert into Hospital values (1002, 'Hospital B', 'password', 'hospitalemail@gmail.com / 4234344', 345356)
insert into Recipient values (2343, 'Ram', 34, 'M', 'O-', 0)

-- Old tables
-- create table if not exists Donor (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), foreign key (HospitalID) references Hospital(HospitalID))
-- create table if not exists Recipient (Name varchar(40), Age int(3), DateOfTransfer date, HospitalID int(4), BloodType char(2), foreign key (HospitalID) references Hospital(HospitalID))