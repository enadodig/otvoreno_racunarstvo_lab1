--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.genre (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.genre OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genre_id_seq OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.genre_id_seq OWNED BY public.genre.id;


--
-- Name: subgenre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subgenre (
    id integer NOT NULL,
    name text NOT NULL,
    genre_id integer
);


ALTER TABLE public.subgenre OWNER TO postgres;

--
-- Name: subgenre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subgenre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subgenre_id_seq OWNER TO postgres;

--
-- Name: subgenre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subgenre_id_seq OWNED BY public.subgenre.id;


--
-- Name: genre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre ALTER COLUMN id SET DEFAULT nextval('public.genre_id_seq'::regclass);


--
-- Name: subgenre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subgenre ALTER COLUMN id SET DEFAULT nextval('public.subgenre_id_seq'::regclass);


--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.genre (id, name) FROM stdin;
1	Rock
2	Pop
3	Country
4	Hip Hop
5	Electronic
6	Jazz
7	Metal
8	Folk
9	R&B
10	Reggae
\.


--
-- Data for Name: subgenre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subgenre (id, name, genre_id) FROM stdin;
1	Hard Rock	1
3	Euro Pop	2
4	Dance Pop	2
6	Bluegrass	3
7	Gangsta Rap	4
8	Hardcore Hip Hop	4
9	Glitch	5
10	Ambient	5
11	Acid Jazz	6
12	Jazz Fusion	6
13	Experimental Metal	7
15	Garage Punk	8
16	Anarcho Punk	8
17	Contemporary R&B	9
18	Soul	9
19	Ska	10
20	Dub	10
2	Alternative Rock	1
5	Singer Songwriter	3
14	Power Metal	7
\.


--
-- Name: genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.genre_id_seq', 10, true);


--
-- Name: subgenre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subgenre_id_seq', 20, true);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: subgenre subgenre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subgenre
    ADD CONSTRAINT subgenre_pkey PRIMARY KEY (id);


--
-- Name: subgenre subgenre_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subgenre
    ADD CONSTRAINT subgenre_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genre(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

