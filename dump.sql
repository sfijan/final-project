--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: competition; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competition (
    id integer NOT NULL,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    public boolean NOT NULL
);


ALTER TABLE public.competition OWNER TO postgres;

--
-- Name: competition_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.competition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.competition_id_seq OWNER TO postgres;

--
-- Name: competition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.competition_id_seq OWNED BY public.competition.id;


--
-- Name: contains; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contains (
    task_id integer,
    competition_id integer
);


ALTER TABLE public.contains OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(256) NOT NULL,
    password_hash character varying(256),
    email character varying(256) NOT NULL,
    admin boolean
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: korisnik_pk_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.korisnik_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.korisnik_pk_seq OWNER TO postgres;

--
-- Name: korisnik_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.korisnik_pk_seq OWNED BY public."user".id;


--
-- Name: language; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.language (
    id integer NOT NULL,
    name text NOT NULL,
    version text NOT NULL
);


ALTER TABLE public.language OWNER TO postgres;

--
-- Name: language_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.language_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.language_id_seq OWNER TO postgres;

--
-- Name: language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.language_id_seq OWNED BY public.language.id;


--
-- Name: participates_in; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participates_in (
    user_id integer,
    competition_id integer
);


ALTER TABLE public.participates_in OWNER TO postgres;

--
-- Name: submission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submission (
    task_id integer NOT NULL,
    user_id integer NOT NULL,
    "time" timestamp without time zone NOT NULL,
    language integer NOT NULL,
    result integer,
    id integer NOT NULL
);


ALTER TABLE public.submission OWNER TO postgres;

--
-- Name: submission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_id_seq OWNER TO postgres;

--
-- Name: submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submission_id_seq OWNED BY public.submission.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task (
    id integer NOT NULL,
    text text NOT NULL,
    title character varying(255) NOT NULL,
    maxpoints integer NOT NULL,
    public boolean NOT NULL,
    time_limit_ms integer,
    memory_limit_kb integer
);


ALTER TABLE public.task OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_seq OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: test; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test (
    input text NOT NULL,
    output text NOT NULL,
    task integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.test OWNER TO postgres;

--
-- Name: test_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_id_seq OWNER TO postgres;

--
-- Name: test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_id_seq OWNED BY public.test.id;


--
-- Name: test_result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_result (
    test_id integer NOT NULL,
    submission_id integer NOT NULL,
    points integer
);


ALTER TABLE public.test_result OWNER TO postgres;

--
-- Name: competition id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competition ALTER COLUMN id SET DEFAULT nextval('public.competition_id_seq'::regclass);


--
-- Name: language id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.language ALTER COLUMN id SET DEFAULT nextval('public.language_id_seq'::regclass);


--
-- Name: submission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission ALTER COLUMN id SET DEFAULT nextval('public.submission_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: test id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test ALTER COLUMN id SET DEFAULT nextval('public.test_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.korisnik_pk_seq'::regclass);


--
-- Data for Name: competition; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.competition (id, start_time, end_time, public) FROM stdin;
\.


--
-- Data for Name: contains; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contains (task_id, competition_id) FROM stdin;
\.


--
-- Data for Name: language; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.language (id, name, version) FROM stdin;
\.


--
-- Data for Name: participates_in; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participates_in (user_id, competition_id) FROM stdin;
\.


--
-- Data for Name: submission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submission (task_id, user_id, "time", language, result, id) FROM stdin;
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (id, text, title, maxpoints, public, time_limit_ms, memory_limit_kb) FROM stdin;
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test (input, output, task, id) FROM stdin;
\.


--
-- Data for Name: test_result; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_result (test_id, submission_id, points) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, password_hash, email, admin) FROM stdin;
\.


--
-- Name: competition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.competition_id_seq', 1, false);


--
-- Name: korisnik_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.korisnik_pk_seq', 1, false);


--
-- Name: language_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.language_id_seq', 1, false);


--
-- Name: submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submission_id_seq', 1, false);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_id_seq', 1, false);


--
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_id_seq', 1, false);


--
-- Name: competition competition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competition
    ADD CONSTRAINT competition_pkey PRIMARY KEY (id);


--
-- Name: user korisnik_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT korisnik_pkey PRIMARY KEY (id);


--
-- Name: language language_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_pkey PRIMARY KEY (id);


--
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: test test_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);


--
-- Name: user unique_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- Name: user unique_user_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT unique_user_email UNIQUE (email);


--
-- Name: user unique_username; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT unique_username UNIQUE (username);


--
-- Name: contains uniqueness; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contains
    ADD CONSTRAINT uniqueness UNIQUE (task_id, competition_id);


--
-- Name: contains contains_competition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contains
    ADD CONSTRAINT contains_competition_id_fkey FOREIGN KEY (competition_id) REFERENCES public.competition(id);


--
-- Name: contains contains_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contains
    ADD CONSTRAINT contains_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id);


--
-- Name: participates_in participates_in_competition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participates_in
    ADD CONSTRAINT participates_in_competition_id_fkey FOREIGN KEY (competition_id) REFERENCES public.competition(id);


--
-- Name: participates_in participates_in_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participates_in
    ADD CONSTRAINT participates_in_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: submission submission_language_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_language_fkey FOREIGN KEY (language) REFERENCES public.language(id);


--
-- Name: submission submission_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id);


--
-- Name: submission submission_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.task(id);


--
-- Name: test_result test_result_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_result
    ADD CONSTRAINT test_result_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(id);


--
-- Name: test_result test_result_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_result
    ADD CONSTRAINT test_result_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.test(id);


--
-- Name: test test_task_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_task_fkey FOREIGN KEY (task) REFERENCES public.task(id);


--
-- PostgreSQL database dump complete
--

