-- Cria uma "pasta" chamada exercicio_alunos dentro do bando de dados atual
CREATE SCHEMA exercicio_alunos;  

-- "Entra" na pasta criada
-- (o comando abaixo so existe no SGBD PostgreSQL)
SET search_path TO exercicio_alunos;  

-- Todas as operacoes abaixo serao realizadas dentro da pasta criada
create table Aluno(
	nroAluno numeric(9,0) primary key,
	nomeAluno varchar(30),
	formacao varchar(25),
	nivel varchar(2),
	idade numeric(3,0)
	);
create table Professor(
	idProf numeric(9,0) primary key,
	nomeProf varchar(30),
	idDepto numeric(2,0)
	);
create table Curso(
	nome varchar(40) primary key,
	horario varchar(20),
	sala varchar(10),
	idProf numeric(9,0),
	foreign key(idProf) references Professor
	);
create table Matriculado(
	nroAluno numeric(9,0),
	nomeCurso varchar(40),
	primary key(nroAluno,nomeCurso),
	foreign key(nroAluno) references Aluno,
	foreign key(nomeCurso) references Curso(nome)
	);


insert into Aluno values(051135593,'Maria White','English','SR',21);
insert into Aluno values(060839453,'Charles Harris','Architecture','SR',22);
insert into Aluno values(099354543,'Susan Martin','Law','JR',20);
insert into Aluno values(112348546,'Joseph Thompson','Computer Science','SO',19);
insert into Aluno values(115987938,'Christopher Garcia','Computer Science','JR',20);
insert into Aluno values(132977562,'Angela Martinez','History','SR',20);
insert into Aluno values(269734834,'Thomas Robinson','Psychology','SO',18);
insert into Aluno values(280158572,'Margaret Clark','Animal Science','FR',18);
insert into Aluno values(301221823,'Juan Rodriguez','Psychology','JR',20);
insert into Aluno values(318548912,'Dorthy Lewis','Finance','FR',18);
insert into Aluno values(320874981,'Daniel Lee','Electrical Engineering','FR',17);
insert into Aluno values(322654189,'Lisa Walker','Computer Science','SO',17);
insert into Aluno values(348121549,'Paul Hall','Computer Science','JR',18);
insert into Aluno values(351565322,'Nancy Allen','Accounting','JR',19);
insert into Aluno values(451519864,'Mark Young','Finance','FR',18);
insert into Aluno values(455798411,'Luis Hernandez','Electrical Engineering','FR',17);
insert into Aluno values(462156489,'Donald King','Mechanical Engineering','SO',19);
insert into Aluno values(550156548,'George Wright','Education','SR',21);
insert into Aluno values(552455318,'Ana Lopez','Computer Engineering','SR',19);
insert into Aluno values(556784565,'Kenneth Hill','Civil Engineering','SR',21);
insert into Aluno values(567354612,'Karen Scott','Computer Engineering','FR',18);
insert into Aluno values(573284895,'Steven Green','Kinesiology','SO',19);
insert into Aluno values(574489456,'Betty Adams','Economics','JR',20);
insert into Aluno values(578875478,'Edward Baker','Veterinary Medicine','SR',21);


insert into Professor values(142519864,'Ivana Teach',20);
insert into Professor values(242518965,'James Smith',68);
insert into Professor values(141582651,'Mary Johnson',20);
insert into Professor values(011564812,'John Williams',68);
insert into Professor values(254099823,'Patricia Jones',68);
insert into Professor values(356187925,'Robert Brown',12);
insert into Professor values(489456522,'Linda Davis',20);
insert into Professor values(287321212,'Michael Miller',12);
insert into Professor values(248965255,'Barbara Wilson',12);
insert into Professor values(159542516,'William Moore',33);
insert into Professor values(090873519,'Elizabeth Taylor',11);
insert into Professor values(486512566,'David Anderson',20);
insert into Professor values(619023588,'Jennifer Thomas',11);
insert into Professor values(489221823,'Richard Jackson',33);
insert into Professor values(548977562,'Ulysses Teach',20);


insert into Curso values('Data Structures','MWF 10','R128',489456522);
insert into Curso values('Database Systems','MWF 12:30-1:45','1320 DCL',142519864);
insert into Curso values('Operating System Design','TuTh 12:30-1:45','20 AVW',489456522); 
insert into Curso values('Archaeology of the Incas','MWF 3-4:15','R128',248965255);
insert into Curso values('Aviation Accident Investigation','TuTh 1-2:50','Q3',011564812);
insert into Curso values('Air Quality Engineering','TuTh 10:30-11:45','R15',011564812);
insert into Curso values('Introductory Latin','MWF 3-4:15','R12',248965255);
insert into Curso values('American Political Parties','TuTh 2-3:15','20 AVW',619023588);
insert into Curso values('Social Cognition','Tu 6:30-8:40','R15',159542516);
insert into Curso values('Perception','MTuWTh 3','Q3',489221823);
insert into Curso values('Multivariate Analysis','TuTh 2-3:15','R15',090873519);
insert into Curso values('Patent Law','F 1-2:50','R128',090873519);
insert into Curso values('Urban Economics','MWF 11','20 AVW',489221823);
insert into Curso values('Organic Chemistry','TuTh 12:30-1:45','R12',489221823);
insert into Curso values('Marketing Research','MW 10-11:15','1320 DCL',489221823);
insert into Curso values('Seminar in American Art','M 4','R15',489221823);
insert into Curso values('Orbital Mechanics','MWF 8','1320 DCL',011564812);
insert into Curso values('Dairy Herd Management','TuTh 12:30-1:45','R128',356187925);
insert into Curso values('Communication Networks','MW 9:30-10:45','20 AVW',141582651);
insert into Curso values('Optical Electronics','TuTh 12:30-1:45','R15',254099823);
insert into Curso values('Intoduction to Math','TuTh 8-9:30','R128',489221823);

insert into Matriculado values(112348546,'Database Systems');
insert into Matriculado values(115987938,'Database Systems');
insert into Matriculado values(348121549,'Database Systems');
insert into Matriculado values(322654189,'Database Systems');
insert into Matriculado values(552455318,'Database Systems');
insert into Matriculado values(455798411,'Operating System Design');
insert into Matriculado values(552455318,'Operating System Design');
insert into Matriculado values(567354612,'Operating System Design');
insert into Matriculado values(112348546,'Operating System Design');
insert into Matriculado values(115987938,'Operating System Design');
insert into Matriculado values(322654189,'Operating System Design');
insert into Matriculado values(567354612,'Data Structures');
insert into Matriculado values(552455318,'Communication Networks');
insert into Matriculado values(455798411,'Optical Electronics');
insert into Matriculado values(301221823,'Perception');
insert into Matriculado values(301221823,'Social Cognition');
insert into Matriculado values(301221823,'American Political Parties');
insert into Matriculado values(556784565,'Air Quality Engineering');
insert into Matriculado values(099354543,'Patent Law');
insert into Matriculado values(574489456,'Urban Economics');
