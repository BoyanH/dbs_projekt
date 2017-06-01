--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: contains; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE contains (
    tweetid bigint NOT NULL,
    hashtagtext character varying(40) NOT NULL
);


ALTER TABLE contains OWNER TO postgres;

--
-- Name: hashtag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE hashtag (
    totalcount integer,
    textlowercase character varying(40) NOT NULL
);


ALTER TABLE hashtag OWNER TO postgres;

--
-- Name: postedin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE postedin (
    tweetid bigint NOT NULL,
    weekstartdate date NOT NULL
);


ALTER TABLE postedin OWNER TO postgres;

--
-- Name: tweet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE tweet (
    author character varying(20) NOT NULL,
    text text NOT NULL,
    "time" date NOT NULL,
    rating real,
    id bigint NOT NULL
);


ALTER TABLE tweet OWNER TO postgres;

--
-- Name: tweet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tweet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tweet_id_seq OWNER TO postgres;

--
-- Name: tweet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tweet_id_seq OWNED BY tweet.id;


--
-- Name: usedin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE usedin (
    count integer,
    hashtagtext character varying(40) NOT NULL,
    weekstartdate date NOT NULL
);


ALTER TABLE usedin OWNER TO postgres;

--
-- Name: usedtogetherwith; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE usedtogetherwith (
    primaryhashtag character varying(40) NOT NULL,
    togetherwithhashtag character varying(40) NOT NULL,
    count integer
);


ALTER TABLE usedtogetherwith OWNER TO postgres;

--
-- Name: week; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE week (
    enddate date NOT NULL,
    startdate date NOT NULL
);


ALTER TABLE week OWNER TO postgres;

--
-- Data for Name: contains; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contains (tweetid, hashtagtext) FROM stdin;
\.


--
-- Data for Name: hashtag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY hashtag (totalcount, textlowercase) FROM stdin;
\.


--
-- Data for Name: postedin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY postedin (tweetid, weekstartdate) FROM stdin;
\.


--
-- Data for Name: tweet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tweet (author, text, "time", rating, id) FROM stdin;
\.


--
-- Name: tweet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tweet_id_seq', 1, false);


--
-- Data for Name: usedin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY usedin (count, hashtagtext, weekstartdate) FROM stdin;
\.


--
-- Data for Name: usedtogetherwith; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY usedtogetherwith (primaryhashtag, togetherwithhashtag, count) FROM stdin;
\.


--
-- Data for Name: week; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY week (enddate, startdate) FROM stdin;
\.


--
-- Name: hashtag hashtag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hashtag
    ADD CONSTRAINT hashtag_pkey PRIMARY KEY (textlowercase);


--
-- Name: tweet tweet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tweet
    ADD CONSTRAINT tweet_pkey PRIMARY KEY (id);


--
-- Name: week week_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY week
    ADD CONSTRAINT week_pkey PRIMARY KEY (startdate);


--
-- Name: contains contains_hashtagtext_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contains
    ADD CONSTRAINT contains_hashtagtext_fkey FOREIGN KEY (hashtagtext) REFERENCES hashtag(textlowercase);


--
-- Name: contains contains_tweetid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contains
    ADD CONSTRAINT contains_tweetid_fkey FOREIGN KEY (tweetid) REFERENCES tweet(id);


--
-- Name: postedin postedin_tweetid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY postedin
    ADD CONSTRAINT postedin_tweetid_fkey FOREIGN KEY (tweetid) REFERENCES tweet(id);


--
-- Name: postedin postedin_weekstartdate_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY postedin
    ADD CONSTRAINT postedin_weekstartdate_fkey FOREIGN KEY (weekstartdate) REFERENCES week(startdate);


--
-- Name: usedin usedin_hashtagtext_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY usedin
    ADD CONSTRAINT usedin_hashtagtext_fkey FOREIGN KEY (hashtagtext) REFERENCES hashtag(textlowercase);


--
-- Name: usedin usedin_weekstartdate_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY usedin
    ADD CONSTRAINT usedin_weekstartdate_fkey FOREIGN KEY (weekstartdate) REFERENCES week(startdate);


--
-- Name: usedtogetherwith usedtogetherwith_primaryhashtag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY usedtogetherwith
    ADD CONSTRAINT usedtogetherwith_primaryhashtag_fkey FOREIGN KEY (primaryhashtag) REFERENCES hashtag(textlowercase);


--
-- Name: usedtogetherwith usedtogetherwith_togetherwithhashtag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY usedtogetherwith
    ADD CONSTRAINT usedtogetherwith_togetherwithhashtag_fkey FOREIGN KEY (togetherwithhashtag) REFERENCES hashtag(textlowercase);


--
-- Name: contains; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE contains TO testuser;


--
-- Name: hashtag; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE hashtag TO testuser;


--
-- Name: postedin; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE postedin TO testuser;


--
-- Name: tweet; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE tweet TO testuser;


--
-- Name: usedin; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE usedin TO testuser;


--
-- Name: usedtogetherwith; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE usedtogetherwith TO testuser;


--
-- Name: week; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE week TO testuser;


--
-- PostgreSQL database dump complete
--

