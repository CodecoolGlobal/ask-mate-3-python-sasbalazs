--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    accepted boolean,
    user_id integer
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text NOT NULL
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    password text,
    registration_time timestamp without time zone
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE ;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE ;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)  ON DELETE CASCADE ;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id)  ON DELETE CASCADE ;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id)  ON DELETE CASCADE ;

INSERT INTO users VALUES (0, 'jonh@doe.com', '$2b$12$oEu70hPGVeKwciKR03EIoe/Y/IK8fojMoACqGO0exGucSq.lIsbim', '2017-04-28 08:29:00');
INSERT INTO users VALUES (4,'magyarorszag@gmail.com', '$2b$12$6IxC.ov9aIlSUa/80m/ljeFvwM6x67p3GSrK7lWlmeUiDnAJFi9SW', '2022-02-02 11:41:55');
INSERT INTO users VALUES (5, 'fightklub@freemail.hu', '$2b$12$EWW4mD6P..4R.6HMfbryLeQhThH/cAs68g153v2sBp/lbvurcaxSW', '2022-02-02 11:46:36');
SELECT pg_catalog.setval('users_id_seq', 1, true);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png');
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', 'canvas.png');
INSERT INTO question VALUES (7, '2022-01-21 01:50:45', 0, 7, 'Is Jason Momoa really single?', 'Hey, girls, did you hear the news, that Jason Momoa will divorce? I can''t believe, they were a dream couple with his wife!!! Who is going to buy a plane_ticket to America? :D','momoa_look.jpg');
INSERT INTO question VALUES (6, '2022-01-21 00:42:50', 0, 5, 'Hey guys, do you have any travel tips?','I have gotten two weeks of holiday, which destination should I choose? Is it a good idea to spend a vacation on the beach, or should I visit the mountains in the beautiful Switzerland?','beachandsun.jpg');
INSERT INTO question VALUES (5, '2022-01-21 00:41:12', 0, 2, 'Why Do Rivers Curve?','Could somebody answer me, why rivers do not stream straight?','curvy_river.jpg');
INSERT INTO question VALUES (4, '2022-01-21 00:36:21', 0, 1, 'Where is a gym in the city?','I am looking for a training center near to 5th Avenue, 78th street corner? Is there a spacious one?', 'happy_minion.jpeg');
INSERT INTO question VALUES (3, '2022-01-21 00:30:32', 0, 3, 'What year Mustang should you avoid?','Do you have a question about Ford Mustang? Ask your question and get expert answers from our inhouse team of car-buffs as well as inputs from thousands of Autoportal readership!', 'mustang.jpg');




SELECT pg_catalog.setval('question_id_seq', 2, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, False);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg', False);
INSERT INTO answer VALUES (3, '2022-01-21 01:37:46', 0, 3, 'Avoid The 2006 Model Year! Produced by Ford Motor Company, an American multinational car corporation, the Ford Mustang is a series of cars manufactured since 1964.',  'Ford-Mustang_2005_Kupeja_162531904_7.jpg', False);
INSERT INTO answer VALUES (4, '2022-01-21 01:38:39', 0, 5, 'A meandering river is a great example of a phenomenon of water changing the shape of land. When it is surrounded by steep rock a river rarely curves but when it open up in large valleys it will weave back and forth. Water on the outside of the river will travel faster and erode the land more quickly. Eventually it will curve too much and lose speed. A stream table can be used to model a meandering river.', NULL, False);
INSERT INTO answer VALUES (5, '2022-01-21 01:39:43', 0, 5, 'Are you kidding me? What kind of silly question is this? Did you not learn geography?', NULL, False);
INSERT INTO answer VALUES (6, '2022-01-21 01:40:52', 0, 6, 'You should definitely visit Switzerland! I recommend you take a trip to Switzerland. It is also possible travel by train between mountains.', 'schweizerbahnen.jpeg', False);
INSERT INTO answer VALUES (8, '2022-01-21 01:56:49', 0, 7, 'I think so... Do you think you can meet him?', 'momoa_single.jpg', False);

SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00');
INSERT INTO comment VALUES (4, NULL, 8, 'What''s with you? if you don''t like the topic can roll down!','2022-01-21 01:59:51', 0);
INSERT INTO comment VALUES (5, NULL, 6, 'Switzerland is f*cking expensive! Don''t go there!', '2022-01-21 02:04:11', 0);
INSERT INTO comment VALUES (6, NULL, 6, 'I really enjoyed the mountains, but yes, the first commentator has right, you''d better go to Austria, or North-Italy.','2022-01-21 02:08:05',1);
INSERT INTO comment VALUES (7, 0, NULL, 'This is extremely short explanation...', '2022-01-21 02:19:21',0);
INSERT INTO comment VALUES (8, NULL, 4, 'As a result of river regulations, many rivers have straightened out.', '2022-01-21 02:25:29',1);
INSERT INTO comment VALUES (9, 7, NULL, 'helloooooooo', '2022-01-21 08:32:24',1);
INSERT INTO comment VALUES (3, NULL, 8, 'Seriously?? Can''t we talk about other things???', '2022-01-21 08:58:07',1);
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
INSERT INTO tag VAlUES (4, 'momoa');
INSERT INTO tag VAlUES (5, 'single');
INSERT INTO tag VAlUES (6, 'single');

SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
INSERT INTO question_tag VALUES (7, 4);
INSERT INTO question_tag VALUES (7, 5);
