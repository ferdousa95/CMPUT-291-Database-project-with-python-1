drop table if exists answers;
drop table if exists questions;
drop table if exists votes;
drop table if exists tags;
drop table if exists posts;
drop table if exists ubadges;
drop table if exists badges;
drop table if exists privileged;
drop table if exists users;

create table users (uid	char(4),
  name		text,
  pwd		text,
  city		text,
  crdate	date,
  primary key (uid)
);
create table privileged (
  uid		char(4),
  primary key (uid),
  foreign key (uid) references users
);
create table badges (
  bname		text,
  type		text,
  primary key (bname)
);
create table ubadges (
  uid		char(4),
  bdate		date,
  bname		text,
  primary key (uid,bdate),
  foreign key (uid) references users,
  foreign key (bname) references badges
);
create table posts (
  pid		char(4),
  pdate		date,
  title		text,
  body		text,
  poster	char(4),
  primary key (pid),
  foreign key (poster) references users
);
create table tags (
  pid		char(4),
  tag		text,
  primary key (pid,tag),
  foreign key (pid) references posts
);
create table votes (
  pid		char(4),
  vno		int,
  vdate		text,
  uid		char(4),
  primary key (pid,vno),
  foreign key (pid) references posts,
  foreign key (uid) references users
);
create table questions (
  pid		char(4),
  theaid	char(4),
  primary key (pid),
  foreign key (theaid) references answers
);
create table answers (
  pid		char(4),
  qid		char(4),
  primary key (pid),
  foreign key (qid) references questions
);
insert into users values
    ('u001',
    'Maksimus Andruchow',
     'peepee',
     'Halifax',
     '2019-12-30');
INSERT INTO users values
    ('u002',
     'Ferdous Ahmed Adit',
     'letmein',
     'Dhaka',
     '2020-10-29');
INSERT INTO privileged values
('u002');
INSERT INTO privileged values
('u001');
INSERT INTO posts VALUES
('p001',
'2020-10-27',
'What is Tidder?',
'I am really trying to figure out what Tidder is.',
'u001');

INSERT INTO posts VALUES
('p002',
'2020-10-27',
'What is a post?',
'I am really trying to figure out how to make a post.',
'u001');

INSERT INTO posts VALUES
    ('p003',
    '2020-10-27',
    'You just posted one.',
    'You are so stupid. You literally just posted one. So dumb.',
    'u001');
INSERT INTO posts VALUES
('p004',
'2020-10-22',
'Who even uses this website?',
'I am really trying to figure out who uses this website.',
'u001');
 INSERT INTO posts VALUES
('p005',
'2020-10-23',
'What is life?',
'I am really trying to figure out what life is.',
'u001');
 INSERT INTO posts VALUES
('p006',
'2020-10-27',
'What is SQLite?',
'I am really trying to figure out what SQLite is.',
'u001');
INSERT INTO posts VALUES
('p007',
'2020-10-27',
'Life is living.',
'Life... can be broken down into living each day by the fullest.',
'u001');
INSERT INTO questions VALUES
('p002', 'p003');
INSERT INTO badges VALUES
('alpha', 'GOLD');
INSERT INTO answers VALUES
    ('p007',
    'p005');
INSERT INTO answers VALUES
    ('p003',
    'p002');
INSERT INTO tags VALUES
    ('p001',
    'awesome');
INSERT INTO tags VALUES
    ('p001',
    'funny');
INSERT INTO votes VALUES
    ('p003',
    1,
    '2020-10-27',
    'yeet');

INSERT INTO votes VALUES
    ('p003',
    2,
    '2020-10-27',
    'boii');


INSERT INTO users VALUES('JoDo', 'John Doe', 'pass12', 'Edmonton', '2012-01-20' );
INSERT INTO users VALUES('MaSm', 'Marry Smith', 'pass23', 'Edmonton', '2013-12-10' );
INSERT INTO users VALUES('SaVa', 'Sara Valle', 'pass34', 'Edmonton', '2016-02-09' );
INSERT INTO users VALUES('EmJo', 'Emma Johnson', 'pass45', 'Edmonton', '2016-08-17' );
INSERT INTO users VALUES('KiAb', 'Kim Abby', 'pass56', 'Edmonton', '2014-11-18' );
INSERT INTO users VALUES('SaEl', 'Sam Elden', 'pass67', 'Edmonton', '2013-03-12' );
INSERT INTO users VALUES('RaLi', 'Rachel Liam', 'pass78', 'Edmonton', '2015-01-08' );
INSERT INTO users VALUES('ErHa', 'Eric Harm', 'pass90', 'Edmonton', '2013-09-23' );
INSERT INTO users VALUES('ElON', 'Ellena ONeil', 'pass10', 'Edmonton', '2014-02-02' );
INSERT INTO users VALUES('AnPa', 'Anna Paul', 'pass19', 'Calgary', '2014-01-23' );
INSERT INTO users VALUES('HeUs', 'Helen Usher', 'pass18', 'Calgary', '2012-09-21' );
INSERT INTO users VALUES('JoPe', 'Joe Pennie', 'pass17', 'Calgary', '2012-10-03' );
INSERT INTO users VALUES('JaMa', 'Jack Maccini', 'pass16', 'Calgary', '2016-02-21' );
INSERT INTO users VALUES('MaRy', 'Mark Ryll', 'pass15', 'Calgary', '2015-08-03' );
INSERT INTO users VALUES('LoXi', 'Loke Xin', 'pass14', 'Calgary', '2015-09-07' );
INSERT INTO users VALUES('LaMa', 'Larry MacConnell', 'pass21', 'Calgary', '2013-02-09' );
INSERT INTO users VALUES('RyRe', 'Ryan Retz', 'pass22', 'Calgary', '2014-04-22' );
INSERT INTO users VALUES('LiRe', 'Lilli Revier', 'pass25', 'Calgary', '2013-05-11' );


INSERT INTO privileged VALUES('MaSm');
INSERT INTO privileged VALUES('EmJo');
INSERT INTO privileged VALUES('SaEl');
INSERT INTO privileged VALUES('ErHa');
INSERT INTO privileged VALUES('AnPa');
INSERT INTO privileged VALUES('JoPe');
INSERT INTO privileged VALUES('MaRy');
INSERT INTO privileged VALUES('LaMa');


INSERT INTO badges VALUES ('socratic question','gold');
INSERT INTO badges VALUES ('stellar question', 'gold');
INSERT INTO badges VALUES ('great answer','gold');
INSERT INTO badges VALUES ('popular answer','gold');
INSERT INTO badges VALUES ('fanatic user','gold');
INSERT INTO badges VALUES ('legendary user','gold');
INSERT INTO badges VALUES ('good question','silver');
INSERT INTO badges VALUES ('good answer','silver');
INSERT INTO badges VALUES ('enthusiast user','silver');
INSERT INTO badges VALUES ('nice question','bronze');
INSERT INTO badges VALUES ('nice answer','bronze');
INSERT INTO badges VALUES ('commentator user','bronze');


INSERT INTO ubadges VALUES('JoDo', '2014-09-25', 'stellar question' );
INSERT INTO ubadges VALUES('MaSm', '2014-10-11', 'commentator user' );
INSERT INTO ubadges VALUES('EmJo', '2017-09-25', 'nice question' );
INSERT INTO ubadges VALUES('SaEl', '2015-09-12', 'good question' );
INSERT INTO ubadges VALUES('SaEl', '2014-09-25', 'good answer' );
INSERT INTO ubadges VALUES('SaEl', '2014-12-09', 'legendary user' );
INSERT INTO ubadges VALUES('JoPe', '2013-09-25', 'good question' );
INSERT INTO ubadges VALUES('JaMa', '2016-12-11', 'good answer' );
INSERT INTO ubadges VALUES('MaRy', '2016-09-25', 'nice question' );
INSERT INTO ubadges VALUES('MaRy', '2018-11-02', 'nice answer' );
INSERT INTO ubadges VALUES('MaRy', '2017-01-19', 'great answer' );
INSERT INTO ubadges VALUES('MaRy', '2017-02-12', 'legendary user' );



INSERT INTO posts VALUES('p123', '2016-10-01', 'mySQL', 'Can we use mySQL for the project?', 'JoDo');
INSERT INTO posts VALUES('p124', '2016-03-04', 'SQLite', 'How can we run SQLite?', 'MaSm');
INSERT INTO posts VALUES('p125', '2016-03-18', 'Help!', 'I need help for my project.', 'MaSm');
INSERT INTO posts VALUES('p127', '2017-05-19', 'NoSQL', 'Which one is better? SQL or NoSQL?', 'LaMa');
INSERT INTO posts VALUES('p128', '2017-06-20', 'Help with assignment', 'I need someone to guide me', 'SaVa');
INSERT INTO posts VALUES('p120', '2015-08-21', 'NoSQL Question', 'Is MongoDB better than Berekly DB?', 'LoXi');
INSERT INTO posts VALUES('p133', '2016-02-19', 'ER', 'Why we should learn ER?', 'RaLi');
INSERT INTO posts VALUES('p134', '2017-02-13', 'Mongo problem', 'I have problem connecting to SQLite', 'MaRy');

INSERT INTO posts VALUES('p213', '2016-11-25', 'No mySQl', 'No, it is not open source', 'JoPe');
INSERT INTO posts VALUES('p214', '2017-01-12', 'Just SQLite', 'SOLite is easier', 'LoXi');
INSERT INTO posts VALUES('p215', '2017-09-25', 'I am here', 'I can help', 'ErHa');
INSERT INTO posts VALUES('p216', '2014-09-25', 'help', 'Let me help', 'LiRe');
INSERT INTO posts VALUES('p217', '2017-08-12', 'nosql', 'I think NoSQL is easier', 'RaLi');
INSERT INTO posts VALUES('p218', '2016-12-21', 'For Sure!', 'MongoDb', 'ElON');
INSERT INTO posts VALUES('p219', '2016-10-02', 'BreklyDB', 'BreklyDB was better before', 'MaRy');
INSERT INTO posts VALUES('p220', '2018-01-12', 'mongodb', 'it is cool', 'LaMa');
INSERT INTO posts VALUES('p221', '2016-03-13', 'ER', 'It is essential and help you develop your skill', 'JoDo');
INSERT INTO posts VALUES('p222', '2017-04-06', 'HELP: port', 'Try different port', 'LiRe');


INSERT INTO questions VALUES ("p123", null),
                             ("p125", null),
                             ("p127", null),
							 ("p120", null),
							 ("p133", null),
							 ("p134", null);

INSERT INTO answers VALUES ("p213", "p123"),
                           ("p214", "p123"),
                           ("p215", "p125"),
                           ("p216", "p125"),
						   ("p217", "p127"),
						   ("p218", "p120"),
                           ("p219", "p120"),
						   ("p220", "p120"),
						   ("p221", "p133"),
						   ("p222", "p134");

UPDATE questions SET theaid = 'p213' where pid = 'p123';
UPDATE questions SET theaid = 'p217' where pid = 'p127';
UPDATE questions SET theaid = 'p220' where pid = 'p120';
UPDATE questions SET theaid = 'p222' where pid = 'p134';


INSERT INTO tags VALUES('p123', 'mySQL' );
INSERT INTO tags VALUES('p123', 'project' );
INSERT INTO tags VALUES('p125', 'project' );
INSERT INTO tags VALUES('p127', 'NoSQL' );
INSERT INTO tags VALUES('p120', 'NoSQL' );
INSERT INTO tags VALUES('p120', 'MongoDB' );
INSERT INTO tags VALUES('p120', 'BreklyDB' );
INSERT INTO tags VALUES('p128', 'Assignment' );
INSERT INTO tags VALUES('p128', 'Emergency' );
INSERT INTO tags VALUES('p133', 'ER' );
INSERT INTO tags VALUES('p134', 'MongoDB' );
INSERT INTO tags VALUES('p134', 'Problem' );
INSERT INTO tags VALUES('p134', 'Help' );
INSERT INTO tags VALUES('p213', 'mySQL' );
INSERT INTO tags VALUES('p215', 'Help' );
INSERT INTO tags VALUES('p218', 'MongoDB' );
INSERT INTO tags VALUES('p221', 'ER' );
INSERT INTO tags VALUES('p222', 'Port' );
INSERT INTO tags VALUES('p222', 'problem' );


INSERT INTO votes VALUES('p123', 14, '2017-04-06', 'LiRe');
INSERT INTO votes VALUES('p123', 15, '2016-12-02', 'JoPe');
INSERT INTO votes VALUES('p124', 16, '2016-04-06', 'ErHa');
INSERT INTO votes VALUES('p128', 17, '2017-11-06', 'EmJo');
INSERT INTO votes VALUES('p128', 18, '2018-10-01', 'LoXi');
INSERT INTO votes VALUES('p128', 21, '2018-01-02', 'HeUs');
INSERT INTO votes VALUES('p133', 22, '2016-10-09', 'AnPa');
INSERT INTO votes VALUES('p134', 23, '2017-12-08', 'JaMa');
INSERT INTO votes VALUES('p134', 24, '2017-12-13', 'SaEl');
INSERT INTO votes VALUES('p213', 25, '2017-02-03', 'LiRe');
INSERT INTO votes VALUES('p214', 31, '2017-09-11', 'ErHa');
INSERT INTO votes VALUES('p215', 32, '2017-12-21', 'EmJo');
INSERT INTO votes VALUES('p215', 33, '2018-09-01', 'LoXi');
INSERT INTO votes VALUES('p218', 41, '2017-01-19', 'AnPa');
INSERT INTO votes VALUES('p220', 42, '2018-02-23', 'RyRe');
INSERT INTO votes VALUES('p220', 43, '2018-08-11', 'LiRe');
INSERT INTO votes VALUES('p222', 44, '2017-04-06', 'KiAb');
