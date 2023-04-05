INSERT INTO account(firstname, lastname, password, email) VALUES ('Alex', 'Lan', '123', 'alexlan@mail.ru');
INSERT INTO account(firstname, lastname, password, email) VALUES ('Alssex', 'Lswwan', '121233', 'al2exlan@mail.ru');
INSERT INTO account(firstname, lastname, password, email) VALUES ('Alsasdex', 'La2n', '12333', 'ale1xlan@mail.ru');
INSERT INTO account(firstname, lastname, password, email) VALUES ('Alasex', 'Lsadan', '12223', 'al22exlan@mail.ru');
INSERT INTO locations(latitude, longitude) VALUES (59.959805, 30.219712);
INSERT INTO locations(latitude, longitude) VALUES (54.959805, 30.219712);
INSERT INTO locations(latitude, longitude) VALUES (39.959805, 30.219712);
INSERT INTO animal(weight,length,height,gender,lifestatus,chippingdatetime,chipperid,chippinglocationid, deathdatetime) VALUES(
2.4, 3.0, 2.45, 'MALE', 'DEAD', '2017-03-14', 1, 1, '2020-03-14');
INSERT INTO animal(weight,length,height,gender,lifestatus,chippingdatetime,chipperid,chippinglocationid) VALUES(
2.4, 3.0, 2.45, 'FEMALE', 'ALIVE', '2017-04-15', 1, 1);
INSERT INTO visited_locations(animal_id,date_of_visit,loc_id) VALUES (1,'2022-12-15',1);
INSERT INTO visited_locations(animal_id,date_of_visit,loc_id) VALUES (1,'2022-12-12',2);
INSERT INTO visited_locations(animal_id,date_of_visit,loc_id) VALUES (2,'2023-02-23',3);
INSERT INTO visited_locations(animal_id,date_of_visit,loc_id) VALUES (2,'2023-01-14',1);
INSERT INTO types(type) VALUES('Forest');
INSERT INTO types(type) VALUES('Cave');
INSERT INTO types(type) VALUES('Desert');
INSERT INTO types(type) VALUES('City');
INSERT INTO animal_types(animal_id,type_id) VALUES (2,1);
INSERT INTO animal_types(animal_id,type_id) VALUES (2,2);
INSERT INTO animal_types(animal_id,type_id) VALUES (1,1);
INSERT INTO animal_types(animal_id,type_id) VALUES (1,3);
INSERT INTO animal_types(animal_id,type_id) VALUES (1,4);