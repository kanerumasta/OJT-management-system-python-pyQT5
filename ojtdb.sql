toc.dat                                                                                             0000600 0004000 0002000 00000045546 14444224114 0014455 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP                           {            ojtdb    14.8    14.8 ;    D           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false         E           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false         F           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false         G           1262    16394    ojtdb    DATABASE     i   CREATE DATABASE ojtdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
    DROP DATABASE ojtdb;
                postgres    false         �            1255    24716    update_total_hours()    FUNCTION       CREATE FUNCTION public.update_total_hours() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  hours_diff INTEGER;
BEGIN
  IF (TG_OP = 'INSERT') THEN
    UPDATE TRAINEE
    SET TOTAL_HOURS_WORKED = TOTAL_HOURS_WORKED + NEW.ATTEND_HOURS_WORKED
    WHERE TRAINEE_ID = NEW.TRAINEE_ID;
  ELSIF (TG_OP = 'UPDATE') THEN
    UPDATE TRAINEE
    SET TOTAL_HOURS_WORKED = TOTAL_HOURS_WORKED + NEW.ATTEND_HOURS_WORKED
    WHERE TRAINEE_ID = NEW.TRAINEE_ID;
ELSIF (TG_OP = 'DELETE') THEN
UPDATE TRAINEE SET TOTAL_HOURS_WORKED = TOTAL_HOURS_WORKED - OLD.ATTEND_HOURS_WORKED 
WHERE TRAINEE_ID = OLD.TRAINEE_ID;
  END IF;
  
  RETURN NEW;
END;
$$;
 +   DROP FUNCTION public.update_total_hours();
       public          postgres    false         �            1259    24698    admin    TABLE     �   CREATE TABLE public.admin (
    admin_username character varying(255),
    admin_firstname character varying(255),
    admin_lastname character varying(255),
    admin_password character varying(255),
    admin_email character varying(255) NOT NULL
);
    DROP TABLE public.admin;
       public         heap    postgres    false         �            1259    24836    admin_setting    TABLE     �   CREATE TABLE public.admin_setting (
    setting_id integer NOT NULL,
    setting_name character varying(255),
    setting_value character varying(255)
);
 !   DROP TABLE public.admin_setting;
       public         heap    postgres    false         �            1259    24835    admin_setting_setting_id_seq    SEQUENCE     �   CREATE SEQUENCE public.admin_setting_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.admin_setting_setting_id_seq;
       public          postgres    false    216         H           0    0    admin_setting_setting_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.admin_setting_setting_id_seq OWNED BY public.admin_setting.setting_id;
          public          postgres    false    215         �            1259    24639 
   attendance    TABLE     .  CREATE TABLE public.attendance (
    trainee_id character varying(50) NOT NULL,
    attend_date date NOT NULL,
    attend_time_in time without time zone,
    attend_time_out time without time zone,
    attend_status character varying(50),
    attend_hours_worked double precision DEFAULT 0 NOT NULL
);
    DROP TABLE public.attendance;
       public         heap    postgres    false         �            1259    24845    auto_logged    TABLE     r   CREATE TABLE public.auto_logged (
    trainee_id character varying(50) NOT NULL,
    logged_date date NOT NULL
);
    DROP TABLE public.auto_logged;
       public         heap    postgres    false         �            1259    16416    registry    TABLE     (  CREATE TABLE public.registry (
    reg_id integer NOT NULL,
    reg_firstname character varying(50),
    reg_lastname character varying(50),
    reg_course character varying(100),
    reg_contact character varying(20),
    reg_email character varying(100),
    school_id character varying(20)
);
    DROP TABLE public.registry;
       public         heap    postgres    false         �            1259    16415    registry_reg_id_seq    SEQUENCE     �   CREATE SEQUENCE public.registry_reg_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.registry_reg_id_seq;
       public          postgres    false    212         I           0    0    registry_reg_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.registry_reg_id_seq OWNED BY public.registry.reg_id;
          public          postgres    false    211         �            1259    16400    school    TABLE     E  CREATE TABLE public.school (
    school_id character varying(20) NOT NULL,
    school_name character varying(100),
    school_address character varying(100),
    school_coordinator character varying(100),
    school_contact character varying(20),
    school_required_time integer,
    school_initial character varying(50)
);
    DROP TABLE public.school;
       public         heap    postgres    false         �            1259    24860    task    TABLE     *  CREATE TABLE public.task (
    task_id integer NOT NULL,
    task_title character varying(255) NOT NULL,
    task_descript text,
    task_due date,
    task_created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    task_status character varying(50) DEFAULT 'ongoing'::character varying
);
    DROP TABLE public.task;
       public         heap    postgres    false         �            1259    24870    task_assignment    TABLE     �   CREATE TABLE public.task_assignment (
    id integer NOT NULL,
    task_id integer NOT NULL,
    assign_status character varying(50) DEFAULT 'pending'::character varying,
    trainee_id character varying(50)
);
 #   DROP TABLE public.task_assignment;
       public         heap    postgres    false         �            1259    24869    task_assignment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.task_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.task_assignment_id_seq;
       public          postgres    false    221         J           0    0    task_assignment_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.task_assignment_id_seq OWNED BY public.task_assignment.id;
          public          postgres    false    220         �            1259    24859    task_task_id_seq    SEQUENCE     �   CREATE SEQUENCE public.task_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.task_task_id_seq;
       public          postgres    false    219         K           0    0    task_task_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.task_task_id_seq OWNED BY public.task.task_id;
          public          postgres    false    218         �            1259    16405    trainee    TABLE     �  CREATE TABLE public.trainee (
    trainee_id character varying(50) NOT NULL,
    trainee_firstname character varying(50),
    trainee_lastname character varying(50),
    trainee_email character varying(100),
    trainee_course character varying(100),
    school_id character varying(20),
    trainee_contact character varying(20),
    total_hours_worked double precision DEFAULT 0
);
    DROP TABLE public.trainee;
       public         heap    postgres    false         �           2604    24839    admin_setting setting_id    DEFAULT     �   ALTER TABLE ONLY public.admin_setting ALTER COLUMN setting_id SET DEFAULT nextval('public.admin_setting_setting_id_seq'::regclass);
 G   ALTER TABLE public.admin_setting ALTER COLUMN setting_id DROP DEFAULT;
       public          postgres    false    215    216    216         �           2604    16419    registry reg_id    DEFAULT     r   ALTER TABLE ONLY public.registry ALTER COLUMN reg_id SET DEFAULT nextval('public.registry_reg_id_seq'::regclass);
 >   ALTER TABLE public.registry ALTER COLUMN reg_id DROP DEFAULT;
       public          postgres    false    212    211    212         �           2604    24863    task task_id    DEFAULT     l   ALTER TABLE ONLY public.task ALTER COLUMN task_id SET DEFAULT nextval('public.task_task_id_seq'::regclass);
 ;   ALTER TABLE public.task ALTER COLUMN task_id DROP DEFAULT;
       public          postgres    false    218    219    219         �           2604    24873    task_assignment id    DEFAULT     x   ALTER TABLE ONLY public.task_assignment ALTER COLUMN id SET DEFAULT nextval('public.task_assignment_id_seq'::regclass);
 A   ALTER TABLE public.task_assignment ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220    221         :          0    24698    admin 
   TABLE DATA           m   COPY public.admin (admin_username, admin_firstname, admin_lastname, admin_password, admin_email) FROM stdin;
    public          postgres    false    214       3386.dat <          0    24836    admin_setting 
   TABLE DATA           P   COPY public.admin_setting (setting_id, setting_name, setting_value) FROM stdin;
    public          postgres    false    216       3388.dat 9          0    24639 
   attendance 
   TABLE DATA           �   COPY public.attendance (trainee_id, attend_date, attend_time_in, attend_time_out, attend_status, attend_hours_worked) FROM stdin;
    public          postgres    false    213       3385.dat =          0    24845    auto_logged 
   TABLE DATA           >   COPY public.auto_logged (trainee_id, logged_date) FROM stdin;
    public          postgres    false    217       3389.dat 8          0    16416    registry 
   TABLE DATA           v   COPY public.registry (reg_id, reg_firstname, reg_lastname, reg_course, reg_contact, reg_email, school_id) FROM stdin;
    public          postgres    false    212       3384.dat 5          0    16400    school 
   TABLE DATA           �   COPY public.school (school_id, school_name, school_address, school_coordinator, school_contact, school_required_time, school_initial) FROM stdin;
    public          postgres    false    209       3381.dat ?          0    24860    task 
   TABLE DATA           g   COPY public.task (task_id, task_title, task_descript, task_due, task_created, task_status) FROM stdin;
    public          postgres    false    219       3391.dat A          0    24870    task_assignment 
   TABLE DATA           Q   COPY public.task_assignment (id, task_id, assign_status, trainee_id) FROM stdin;
    public          postgres    false    221       3393.dat 6          0    16405    trainee 
   TABLE DATA           �   COPY public.trainee (trainee_id, trainee_firstname, trainee_lastname, trainee_email, trainee_course, school_id, trainee_contact, total_hours_worked) FROM stdin;
    public          postgres    false    210       3382.dat L           0    0    admin_setting_setting_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.admin_setting_setting_id_seq', 1, true);
          public          postgres    false    215         M           0    0    registry_reg_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.registry_reg_id_seq', 41, true);
          public          postgres    false    211         N           0    0    task_assignment_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.task_assignment_id_seq', 106, true);
          public          postgres    false    220         O           0    0    task_task_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.task_task_id_seq', 47, true);
          public          postgres    false    218         �           2606    24704    admin admin_name_unique 
   CONSTRAINT     m   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_name_unique UNIQUE (admin_firstname, admin_lastname);
 A   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_name_unique;
       public            postgres    false    214    214         �           2606    24843     admin_setting admin_setting_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.admin_setting
    ADD CONSTRAINT admin_setting_pkey PRIMARY KEY (setting_id);
 J   ALTER TABLE ONLY public.admin_setting DROP CONSTRAINT admin_setting_pkey;
       public            postgres    false    216         �           2606    24708    admin admin_username_unique 
   CONSTRAINT     `   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_username_unique UNIQUE (admin_username);
 E   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_username_unique;
       public            postgres    false    214         �           2606    24650    attendance attendance_pk 
   CONSTRAINT     k   ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_pk PRIMARY KEY (trainee_id, attend_date);
 B   ALTER TABLE ONLY public.attendance DROP CONSTRAINT attendance_pk;
       public            postgres    false    213    213         �           2606    24849    auto_logged auto_logged_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.auto_logged
    ADD CONSTRAINT auto_logged_pkey PRIMARY KEY (trainee_id, logged_date);
 F   ALTER TABLE ONLY public.auto_logged DROP CONSTRAINT auto_logged_pkey;
       public            postgres    false    217    217         �           2606    16421    registry registry_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.registry
    ADD CONSTRAINT registry_pkey PRIMARY KEY (reg_id);
 @   ALTER TABLE ONLY public.registry DROP CONSTRAINT registry_pkey;
       public            postgres    false    212         �           2606    16404    school school_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.school
    ADD CONSTRAINT school_pkey PRIMARY KEY (school_id);
 <   ALTER TABLE ONLY public.school DROP CONSTRAINT school_pkey;
       public            postgres    false    209         �           2606    24877 $   task_assignment task_assignment_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.task_assignment
    ADD CONSTRAINT task_assignment_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.task_assignment DROP CONSTRAINT task_assignment_pkey;
       public            postgres    false    221         �           2606    24867    task task_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (task_id);
 8   ALTER TABLE ONLY public.task DROP CONSTRAINT task_pkey;
       public            postgres    false    219         �           2606    16428    trainee trainee_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.trainee
    ADD CONSTRAINT trainee_pkey PRIMARY KEY (trainee_id);
 >   ALTER TABLE ONLY public.trainee DROP CONSTRAINT trainee_pkey;
       public            postgres    false    210         �           2606    24627    trainee unique_email 
   CONSTRAINT     X   ALTER TABLE ONLY public.trainee
    ADD CONSTRAINT unique_email UNIQUE (trainee_email);
 >   ALTER TABLE ONLY public.trainee DROP CONSTRAINT unique_email;
       public            postgres    false    210         �           2606    24631    registry unique_name 
   CONSTRAINT     f   ALTER TABLE ONLY public.registry
    ADD CONSTRAINT unique_name UNIQUE (reg_firstname, reg_lastname);
 >   ALTER TABLE ONLY public.registry DROP CONSTRAINT unique_name;
       public            postgres    false    212    212         �           2606    24633    registry unique_reg_email 
   CONSTRAINT     Y   ALTER TABLE ONLY public.registry
    ADD CONSTRAINT unique_reg_email UNIQUE (reg_email);
 C   ALTER TABLE ONLY public.registry DROP CONSTRAINT unique_reg_email;
       public            postgres    false    212         �           2620    24858 !   attendance trg_update_total_hours    TRIGGER     �   CREATE TRIGGER trg_update_total_hours AFTER INSERT OR DELETE OR UPDATE OF attend_hours_worked ON public.attendance FOR EACH ROW EXECUTE FUNCTION public.update_total_hours();
 :   DROP TRIGGER trg_update_total_hours ON public.attendance;
       public          postgres    false    213    233    213         �           2606    24651     attendance attendance_trainee_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_trainee_fk FOREIGN KEY (trainee_id) REFERENCES public.trainee(trainee_id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.attendance DROP CONSTRAINT attendance_trainee_fk;
       public          postgres    false    3212    210    213         �           2606    24904 '   auto_logged auto_logged_trainee_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.auto_logged
    ADD CONSTRAINT auto_logged_trainee_id_fkey FOREIGN KEY (trainee_id) REFERENCES public.trainee(trainee_id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.auto_logged DROP CONSTRAINT auto_logged_trainee_id_fkey;
       public          postgres    false    217    3212    210         �           2606    16422     registry registry_school_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.registry
    ADD CONSTRAINT registry_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.school(school_id);
 J   ALTER TABLE ONLY public.registry DROP CONSTRAINT registry_school_id_fkey;
       public          postgres    false    212    209    3210         �           2606    24897 ,   task_assignment task_assignment_task_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_assignment
    ADD CONSTRAINT task_assignment_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(task_id) ON DELETE CASCADE;
 V   ALTER TABLE ONLY public.task_assignment DROP CONSTRAINT task_assignment_task_id_fkey;
       public          postgres    false    3232    221    219         �           2606    24910 /   task_assignment task_assignment_trainee_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_assignment
    ADD CONSTRAINT task_assignment_trainee_id_fkey FOREIGN KEY (trainee_id) REFERENCES public.trainee(trainee_id) ON DELETE CASCADE;
 Y   ALTER TABLE ONLY public.task_assignment DROP CONSTRAINT task_assignment_trainee_id_fkey;
       public          postgres    false    3212    221    210         �           2606    24619    trainee trainee_school_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.trainee
    ADD CONSTRAINT trainee_school_fkey FOREIGN KEY (school_id) REFERENCES public.school(school_id) ON UPDATE CASCADE ON DELETE CASCADE;
 E   ALTER TABLE ONLY public.trainee DROP CONSTRAINT trainee_school_fkey;
       public          postgres    false    209    3210    210                                                                                                                                                                  3386.dat                                                                                            0000600 0004000 0002000 00000000055 14444224114 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        admin	admin	admin	admin	admin@gmail.com
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   3388.dat                                                                                            0000600 0004000 0002000 00000000035 14444224114 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	auto-log-out	10:56 am
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   3385.dat                                                                                            0000600 0004000 0002000 00000000524 14444224114 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        07255735	2023-06-18	08:00:00	21:59:42.463046	\N	18.34
24676359	2023-06-19	05:26:30.277767	21:49:42.461744	\N	16.386717771388888
95964482	2023-06-19	21:27:31.277767	21:52:43.91641	\N	0.4201774008333333
35929172	2023-06-19	21:39:10.664211	21:52:53.00745	\N	0.2284286775
07255735	2023-06-19	10:00:00	21:56:29.744495	\N	11.941595693055556
\.


                                                                                                                                                                            3389.dat                                                                                            0000600 0004000 0002000 00000000005 14444224114 0014253 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        \.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3384.dat                                                                                            0000600 0004000 0002000 00000000107 14444224114 0014251 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        40	johnson	trackman	programming	098458467584	js@gmail.com	6583467
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                         3381.dat                                                                                            0000600 0004000 0002000 00000000457 14444224114 0014256 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        12345678	tagum sur national high school	tagum sur, trinidad, bohol	democrito manalili	09845459454	200	tsnhs
87654321	soom national high school	soom, trinidad, bohol	mike tyson	0985948754	300	sis
6583467	ubay national science high school	poblacion,ubay, bohol	jonathan wayamu	09348594574	250	 unshs
\.


                                                                                                                                                                                                                 3391.dat                                                                                            0000600 0004000 0002000 00000001452 14444224114 0014253 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        39	this is first task	this is the detail of first task	2023-06-21	2023-06-19 22:12:25.592981	completed
40	this is second task	second task detail	2023-06-29	2023-06-19 22:13:20.027953	completed
42	this is fourth task	fourth task\ndetail	2023-06-23	2023-06-19 23:32:04.570683	completed
41	this is third task	this is third task description	2023-06-22	2023-06-19 23:29:43.506938	completed
43	new task now	this is a new task for now	2023-06-22	2023-06-19 23:47:04.484483	completed
44	bag ong task ni	bag ong task description	2023-06-18	2023-06-19 23:48:29.868732	late
45	new task na pd ni	this is\ndetail\nof this task	2023-06-22	2023-06-20 00:16:52.605518	completed
46	thsaposidfa	fa0dshfiolsd	2023-06-20	2023-06-20 01:41:07.873831	ongoing
47	shdkfd	fadoshifnl	2023-06-20	2023-06-20 01:55:27.395005	completed
\.


                                                                                                                                                                                                                      3393.dat                                                                                            0000600 0004000 0002000 00000000757 14444224114 0014264 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        86	39	pending	24676359
87	39	pending	95964482
88	39	pending	35929172
89	40	pending	77362450
90	40	pending	07255735
91	41	pending	24676359
92	41	pending	95964482
93	41	pending	07255735
94	42	pending	24676359
95	42	pending	35929172
96	43	pending	24676359
97	44	pending	95964482
98	45	pending	24676359
99	45	pending	07255735
100	46	pending	24676359
101	46	pending	95964482
102	47	pending	77362450
103	47	pending	24676359
104	47	pending	95964482
105	47	pending	35929172
106	47	pending	07255735
\.


                 3382.dat                                                                                            0000600 0004000 0002000 00000000625 14444224114 0014254 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        77362450	miya	panaconda	miya@gmail.com	cookery	87654321	\N	0
24676359	lolita	hammer	lolita@gmail.com	programming	87654321	\N	32.748373101666665
95964482	vexana	hapon	new@gmail.com	programming	6583467	\N	0.8271498930555555
35929172	zilong	runnerman	silong@gmail.com	electronics servicing	12345678	\N	0.4184773105555556
07255735	bane	tagadagat	bane@gmail.com	programming	12345678	\N	30.281595693055557
\.


                                                                                                           restore.sql                                                                                         0000600 0004000 0002000 00000037425 14444224114 0015377 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.8
-- Dumped by pg_dump version 14.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE ojtdb;
--
-- Name: ojtdb; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE ojtdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';


ALTER DATABASE ojtdb OWNER TO postgres;

\connect ojtdb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: update_total_hours(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_total_hours() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  hours_diff INTEGER;
BEGIN
  IF (TG_OP = 'INSERT') THEN
    UPDATE TRAINEE
    SET TOTAL_HOURS_WORKED = TOTAL_HOURS_WORKED + NEW.ATTEND_HOURS_WORKED
    WHERE TRAINEE_ID = NEW.TRAINEE_ID;
  ELSIF (TG_OP = 'UPDATE') THEN
    UPDATE TRAINEE
    SET TOTAL_HOURS_WORKED = TOTAL_HOURS_WORKED + NEW.ATTEND_HOURS_WORKED
    WHERE TRAINEE_ID = NEW.TRAINEE_ID;
ELSIF (TG_OP = 'DELETE') THEN
UPDATE TRAINEE SET TOTAL_HOURS_WORKED = TOTAL_HOURS_WORKED - OLD.ATTEND_HOURS_WORKED 
WHERE TRAINEE_ID = OLD.TRAINEE_ID;
  END IF;
  
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_total_hours() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    admin_username character varying(255),
    admin_firstname character varying(255),
    admin_lastname character varying(255),
    admin_password character varying(255),
    admin_email character varying(255) NOT NULL
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: admin_setting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin_setting (
    setting_id integer NOT NULL,
    setting_name character varying(255),
    setting_value character varying(255)
);


ALTER TABLE public.admin_setting OWNER TO postgres;

--
-- Name: admin_setting_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admin_setting_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.admin_setting_setting_id_seq OWNER TO postgres;

--
-- Name: admin_setting_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admin_setting_setting_id_seq OWNED BY public.admin_setting.setting_id;


--
-- Name: attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendance (
    trainee_id character varying(50) NOT NULL,
    attend_date date NOT NULL,
    attend_time_in time without time zone,
    attend_time_out time without time zone,
    attend_status character varying(50),
    attend_hours_worked double precision DEFAULT 0 NOT NULL
);


ALTER TABLE public.attendance OWNER TO postgres;

--
-- Name: auto_logged; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auto_logged (
    trainee_id character varying(50) NOT NULL,
    logged_date date NOT NULL
);


ALTER TABLE public.auto_logged OWNER TO postgres;

--
-- Name: registry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.registry (
    reg_id integer NOT NULL,
    reg_firstname character varying(50),
    reg_lastname character varying(50),
    reg_course character varying(100),
    reg_contact character varying(20),
    reg_email character varying(100),
    school_id character varying(20)
);


ALTER TABLE public.registry OWNER TO postgres;

--
-- Name: registry_reg_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.registry_reg_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.registry_reg_id_seq OWNER TO postgres;

--
-- Name: registry_reg_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.registry_reg_id_seq OWNED BY public.registry.reg_id;


--
-- Name: school; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school (
    school_id character varying(20) NOT NULL,
    school_name character varying(100),
    school_address character varying(100),
    school_coordinator character varying(100),
    school_contact character varying(20),
    school_required_time integer,
    school_initial character varying(50)
);


ALTER TABLE public.school OWNER TO postgres;

--
-- Name: task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task (
    task_id integer NOT NULL,
    task_title character varying(255) NOT NULL,
    task_descript text,
    task_due date,
    task_created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    task_status character varying(50) DEFAULT 'ongoing'::character varying
);


ALTER TABLE public.task OWNER TO postgres;

--
-- Name: task_assignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_assignment (
    id integer NOT NULL,
    task_id integer NOT NULL,
    assign_status character varying(50) DEFAULT 'pending'::character varying,
    trainee_id character varying(50)
);


ALTER TABLE public.task_assignment OWNER TO postgres;

--
-- Name: task_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_assignment_id_seq OWNER TO postgres;

--
-- Name: task_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_assignment_id_seq OWNED BY public.task_assignment.id;


--
-- Name: task_task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_task_id_seq OWNER TO postgres;

--
-- Name: task_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_task_id_seq OWNED BY public.task.task_id;


--
-- Name: trainee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trainee (
    trainee_id character varying(50) NOT NULL,
    trainee_firstname character varying(50),
    trainee_lastname character varying(50),
    trainee_email character varying(100),
    trainee_course character varying(100),
    school_id character varying(20),
    trainee_contact character varying(20),
    total_hours_worked double precision DEFAULT 0
);


ALTER TABLE public.trainee OWNER TO postgres;

--
-- Name: admin_setting setting_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_setting ALTER COLUMN setting_id SET DEFAULT nextval('public.admin_setting_setting_id_seq'::regclass);


--
-- Name: registry reg_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registry ALTER COLUMN reg_id SET DEFAULT nextval('public.registry_reg_id_seq'::regclass);


--
-- Name: task task_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task ALTER COLUMN task_id SET DEFAULT nextval('public.task_task_id_seq'::regclass);


--
-- Name: task_assignment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignment ALTER COLUMN id SET DEFAULT nextval('public.task_assignment_id_seq'::regclass);


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin (admin_username, admin_firstname, admin_lastname, admin_password, admin_email) FROM stdin;
\.
COPY public.admin (admin_username, admin_firstname, admin_lastname, admin_password, admin_email) FROM '$$PATH$$/3386.dat';

--
-- Data for Name: admin_setting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin_setting (setting_id, setting_name, setting_value) FROM stdin;
\.
COPY public.admin_setting (setting_id, setting_name, setting_value) FROM '$$PATH$$/3388.dat';

--
-- Data for Name: attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attendance (trainee_id, attend_date, attend_time_in, attend_time_out, attend_status, attend_hours_worked) FROM stdin;
\.
COPY public.attendance (trainee_id, attend_date, attend_time_in, attend_time_out, attend_status, attend_hours_worked) FROM '$$PATH$$/3385.dat';

--
-- Data for Name: auto_logged; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auto_logged (trainee_id, logged_date) FROM stdin;
\.
COPY public.auto_logged (trainee_id, logged_date) FROM '$$PATH$$/3389.dat';

--
-- Data for Name: registry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.registry (reg_id, reg_firstname, reg_lastname, reg_course, reg_contact, reg_email, school_id) FROM stdin;
\.
COPY public.registry (reg_id, reg_firstname, reg_lastname, reg_course, reg_contact, reg_email, school_id) FROM '$$PATH$$/3384.dat';

--
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school (school_id, school_name, school_address, school_coordinator, school_contact, school_required_time, school_initial) FROM stdin;
\.
COPY public.school (school_id, school_name, school_address, school_coordinator, school_contact, school_required_time, school_initial) FROM '$$PATH$$/3381.dat';

--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (task_id, task_title, task_descript, task_due, task_created, task_status) FROM stdin;
\.
COPY public.task (task_id, task_title, task_descript, task_due, task_created, task_status) FROM '$$PATH$$/3391.dat';

--
-- Data for Name: task_assignment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_assignment (id, task_id, assign_status, trainee_id) FROM stdin;
\.
COPY public.task_assignment (id, task_id, assign_status, trainee_id) FROM '$$PATH$$/3393.dat';

--
-- Data for Name: trainee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trainee (trainee_id, trainee_firstname, trainee_lastname, trainee_email, trainee_course, school_id, trainee_contact, total_hours_worked) FROM stdin;
\.
COPY public.trainee (trainee_id, trainee_firstname, trainee_lastname, trainee_email, trainee_course, school_id, trainee_contact, total_hours_worked) FROM '$$PATH$$/3382.dat';

--
-- Name: admin_setting_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admin_setting_setting_id_seq', 1, true);


--
-- Name: registry_reg_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.registry_reg_id_seq', 41, true);


--
-- Name: task_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_assignment_id_seq', 106, true);


--
-- Name: task_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_task_id_seq', 47, true);


--
-- Name: admin admin_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_name_unique UNIQUE (admin_firstname, admin_lastname);


--
-- Name: admin_setting admin_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_setting
    ADD CONSTRAINT admin_setting_pkey PRIMARY KEY (setting_id);


--
-- Name: admin admin_username_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_username_unique UNIQUE (admin_username);


--
-- Name: attendance attendance_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_pk PRIMARY KEY (trainee_id, attend_date);


--
-- Name: auto_logged auto_logged_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auto_logged
    ADD CONSTRAINT auto_logged_pkey PRIMARY KEY (trainee_id, logged_date);


--
-- Name: registry registry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registry
    ADD CONSTRAINT registry_pkey PRIMARY KEY (reg_id);


--
-- Name: school school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school
    ADD CONSTRAINT school_pkey PRIMARY KEY (school_id);


--
-- Name: task_assignment task_assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignment
    ADD CONSTRAINT task_assignment_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (task_id);


--
-- Name: trainee trainee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trainee
    ADD CONSTRAINT trainee_pkey PRIMARY KEY (trainee_id);


--
-- Name: trainee unique_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trainee
    ADD CONSTRAINT unique_email UNIQUE (trainee_email);


--
-- Name: registry unique_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registry
    ADD CONSTRAINT unique_name UNIQUE (reg_firstname, reg_lastname);


--
-- Name: registry unique_reg_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registry
    ADD CONSTRAINT unique_reg_email UNIQUE (reg_email);


--
-- Name: attendance trg_update_total_hours; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_total_hours AFTER INSERT OR DELETE OR UPDATE OF attend_hours_worked ON public.attendance FOR EACH ROW EXECUTE FUNCTION public.update_total_hours();


--
-- Name: attendance attendance_trainee_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_trainee_fk FOREIGN KEY (trainee_id) REFERENCES public.trainee(trainee_id) ON DELETE CASCADE;


--
-- Name: auto_logged auto_logged_trainee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auto_logged
    ADD CONSTRAINT auto_logged_trainee_id_fkey FOREIGN KEY (trainee_id) REFERENCES public.trainee(trainee_id) ON DELETE CASCADE;


--
-- Name: registry registry_school_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registry
    ADD CONSTRAINT registry_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.school(school_id);


--
-- Name: task_assignment task_assignment_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignment
    ADD CONSTRAINT task_assignment_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(task_id) ON DELETE CASCADE;


--
-- Name: task_assignment task_assignment_trainee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignment
    ADD CONSTRAINT task_assignment_trainee_id_fkey FOREIGN KEY (trainee_id) REFERENCES public.trainee(trainee_id) ON DELETE CASCADE;


--
-- Name: trainee trainee_school_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trainee
    ADD CONSTRAINT trainee_school_fkey FOREIGN KEY (school_id) REFERENCES public.school(school_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           