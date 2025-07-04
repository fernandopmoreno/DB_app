

CREATE TABLE residencia (
    residencia_id SERIAL PRIMARY KEY,
    isla VARCHAR(20),
    municipio VARCHAR(50),
    empadronamiento VARCHAR(50),
    UNIQUE (isla, municipio, empadronamiento)
);
ALTER TABLE public.residencia ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on residencia for authenticated users" 
ON residencia 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on residencia for authenticated users" 
ON residencia 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on residencia for authenticated users" 
ON residencia 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on residencia for authenticated users" 
ON residencia 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);



CREATE TABLE empleos (
    empleo_id SERIAL PRIMARY KEY,
    trabajo VARCHAR(200),
    estudios VARCHAR(250),
    UNIQUE (trabajo, estudios)
);
ALTER TABLE public.empleos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on empleos for authenticated users" 
ON empleos 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on empleos for authenticated users" 
ON empleos 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on empleos for authenticated users" 
ON empleos 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on empleos for authenticated users" 
ON empleos 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);




CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    dni VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    birth_date DATE,
    residencia_id INT,
    empleo_id INT,
    FOREIGN KEY (residencia_id) REFERENCES residencia (residencia_id),
    FOREIGN KEY (empleo_id) REFERENCES empleos (empleo_id)
);
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on users for authenticated users" 
ON users 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on users for authenticated users" 
ON users 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on users for authenticated users" 
ON users 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on users for authenticated users" 
ON users 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);


CREATE TABLE papeles (
    papel_id SERIAL PRIMARY KEY,
    papel VARCHAR(200) UNIQUE
);
ALTER TABLE public.papeles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on papeles for authenticated users" 
ON papeles 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on papeles for authenticated users" 
ON papeles 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on papeles for authenticated users" 
ON papeles 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on papeles for authenticated users" 
ON papeles 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);



CREATE TABLE secciones (
    seccion_id SERIAL PRIMARY KEY,
    seccion VARCHAR(200) UNIQUE
);
ALTER TABLE public.secciones ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on secciones for authenticated users" 
ON secciones 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on secciones for authenticated users" 
ON secciones 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on secciones for authenticated users" 
ON secciones 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on secciones for authenticated users" 
ON secciones 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);


CREATE TABLE agrupaciones (
    agrupacion_id SERIAL PRIMARY KEY,
    agrupacion VARCHAR(200) UNIQUE
);
ALTER TABLE public.agrupaciones ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on agrupaciones for authenticated users" 
ON agrupaciones 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on agrupaciones for authenticated users" 
ON agrupaciones 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on agrupaciones for authenticated users" 
ON agrupaciones 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on agrupaciones for authenticated users" 
ON agrupaciones 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);


CREATE TABLE estructura (
    estructura_id SERIAL PRIMARY KEY,
    user_id INT,
    papel_id INT,
    agrupacion_id INT,
    seccion_id INT,
    activo BOOLEAN NOT NULL DEFAULT FALSE,
    atril INTEGER,
    programa_anterior BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (user_id, papel_id, agrupacion_id, seccion_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (papel_id) REFERENCES papeles (papel_id),
    FOREIGN KEY (agrupacion_id) REFERENCES agrupaciones (agrupacion_id),
    FOREIGN KEY (seccion_id) REFERENCES secciones (seccion_id)
);
ALTER TABLE public.estructura ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on estructura for authenticated users" 
ON estructura 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on estructura for authenticated users" 
ON estructura 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on estructura for authenticated users" 
ON estructura 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on estructura for authenticated users" 
ON estructura 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);



CREATE TABLE matriculas (
    matricula_id SERIAL PRIMARY KEY,
    matricula_number VARCHAR NOT NULL UNIQUE,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
ALTER TABLE public.matriculas ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow select on matriculas for authenticated users" 
ON matriculas 
FOR SELECT 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);

CREATE POLICY "Allow insert on matriculas for authenticated users" 
ON matriculas 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Allow update on matriculas for authenticated users" 
ON matriculas 
FOR UPDATE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL) 
WITH CHECK (true);

CREATE POLICY "Allow delete on matriculas for authenticated users" 
ON matriculas 
FOR DELETE 
TO authenticated 
USING ((select auth.uid()) IS NOT NULL);


-- Crear la vista all_data
CREATE VIEW all_data with (security_invoker = on) AS
SELECT DISTINCT
    estructura.estructura_id AS estructura_id,
    users.user_id AS user_id,
    users.name AS name,
    users.surname AS surname,
    users.dni AS dni,
    users.email AS email,
    users.phone AS phone,
    users.birth_date AS birth_date,
    papeles.papel AS papel,
    agrupaciones.agrupacion AS agrupacion,
    secciones.seccion AS seccion,
    estructura.activo AS activo,
    estructura.atril AS atril,
    residencia.isla AS isla,
    residencia.municipio AS municipio,
    residencia.empadronamiento AS empadronamiento,
    empleos.trabajo AS trabajo,
    empleos.estudios AS estudios,
    matriculas.matricula_number AS matricula_number
FROM 
    users
    JOIN estructura ON users.user_id = estructura.user_id
    JOIN papeles ON estructura.papel_id = papeles.papel_id
    JOIN agrupaciones ON estructura.agrupacion_id = agrupaciones.agrupacion_id
    JOIN secciones ON estructura.seccion_id = secciones.seccion_id
    LEFT JOIN residencia ON users.residencia_id = residencia.residencia_id
    LEFT JOIN empleos ON users.empleo_id = empleos.empleo_id
    LEFT JOIN matriculas ON users.user_id = matriculas.user_id;

CREATE OR REPLACE FUNCTION insert_into_all_data()
RETURNS TRIGGER AS $$
DECLARE
    v_user_id INTEGER;
    v_papel_id INTEGER;
    v_agrupacion_id INTEGER;
    v_seccion_id INTEGER;
    v_estructura_id INTEGER;
    v_residencia_id INTEGER;
    v_empleo_id INTEGER;
BEGIN
    SELECT user_id INTO v_user_id FROM users WHERE dni = NEW.dni;
    IF v_user_id IS NULL THEN
        INSERT INTO users (name, surname, dni, email, phone, birth_date) 
        VALUES (NEW.name, NEW.surname, NEW.dni, NEW.email, NEW.phone, NEW.birth_date) 
        RETURNING user_id INTO v_user_id;
    END IF;

    -- Get or insert papel, agrupacion, seccion
    SELECT papel_id INTO v_papel_id FROM papeles WHERE papel = NEW.papel;
    IF v_papel_id IS NULL THEN
        INSERT INTO papeles (papel) VALUES (NEW.papel) RETURNING papel_id INTO v_papel_id;
    END IF;

    SELECT agrupacion_id INTO v_agrupacion_id FROM agrupaciones WHERE agrupacion = NEW.agrupacion;
    IF v_agrupacion_id IS NULL THEN
        INSERT INTO agrupaciones (agrupacion) VALUES (NEW.agrupacion) RETURNING agrupacion_id INTO v_agrupacion_id;
    END IF;

    SELECT seccion_id INTO v_seccion_id FROM secciones WHERE seccion = NEW.seccion;
    IF v_seccion_id IS NULL THEN
        INSERT INTO secciones (seccion) VALUES (NEW.seccion) RETURNING seccion_id INTO v_seccion_id;
    END IF;

    -- Insert into estructura
    INSERT INTO estructura (user_id, papel_id, agrupacion_id, seccion_id, activo, atril)
    VALUES (v_user_id, v_papel_id, v_agrupacion_id, v_seccion_id, NEW.activo, NEW.atril)
    RETURNING estructura_id INTO v_estructura_id;

    -- Insert or get residencia
    SELECT residencia_id INTO v_residencia_id
    FROM residencia
    WHERE isla = NEW.isla AND municipio = NEW.municipio AND empadronamiento = NEW.empadronamiento;

    IF v_residencia_id IS NULL THEN
        INSERT INTO residencia (isla, municipio, empadronamiento)
        VALUES (NEW.isla, NEW.municipio, NEW.empadronamiento)
        ON CONFLICT (isla, municipio, empadronamiento) DO NOTHING
        RETURNING residencia_id INTO v_residencia_id;

        IF v_residencia_id IS NULL THEN
            SELECT residencia_id INTO v_residencia_id
            FROM residencia
            WHERE isla = NEW.isla AND municipio = NEW.municipio AND empadronamiento = NEW.empadronamiento;
        END IF;
    END IF;

    UPDATE users SET residencia_id = v_residencia_id WHERE user_id = v_user_id;

    -- Insert or get empleos
    SELECT empleo_id INTO v_empleo_id FROM empleos WHERE trabajo = NEW.trabajo AND estudios = NEW.estudios;
    IF v_empleo_id IS NULL THEN
        INSERT INTO empleos (trabajo, estudios)
        VALUES (NEW.trabajo, NEW.estudios)
        ON CONFLICT (trabajo, estudios) DO NOTHING
        RETURNING empleo_id INTO v_empleo_id;
        IF v_empleo_id IS NULL THEN
            SELECT empleo_id INTO v_empleo_id
            FROM empleos
            WHERE trabajo = NEW.trabajo AND estudios = NEW.estudios;
        END IF;
    END IF;

    UPDATE users SET empleo_id = v_empleo_id WHERE user_id = v_user_id;

    -- Insert into matriculas only if not exists
    IF NEW.matricula_number IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM matriculas WHERE matricula_number = NEW.matricula_number AND user_id = v_user_id
        ) THEN
            INSERT INTO matriculas (matricula_number, user_id)
            VALUES (NEW.matricula_number, v_user_id)
            ON CONFLICT (matricula_number) DO NOTHING;
        END IF;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


-- Crear el trigger INSTEAD OF INSERT para la vista all_data
CREATE TRIGGER insert_all_data_trigger
INSTEAD OF INSERT ON all_data
FOR EACH ROW
EXECUTE FUNCTION insert_into_all_data();

-- Crear la función update_all_data
CREATE OR REPLACE FUNCTION update_all_data()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.name IS DISTINCT FROM OLD.name THEN
        UPDATE users SET name = NEW.name WHERE user_id = OLD.user_id;
    END IF;
    IF NEW.surname IS DISTINCT FROM OLD.surname THEN
        UPDATE users SET surname = NEW.surname WHERE user_id = OLD.user_id;
    END IF;
    IF NEW.dni IS DISTINCT FROM OLD.dni THEN
        UPDATE users SET dni = NEW.dni WHERE user_id = OLD.user_id;
    END IF;
    IF NEW.email IS DISTINCT FROM OLD.email THEN
        UPDATE users SET email = NEW.email WHERE user_id = OLD.user_id;
    END IF;
    IF NEW.phone IS DISTINCT FROM OLD.phone THEN
        UPDATE users SET phone = NEW.phone WHERE user_id = OLD.user_id;
    END IF;
    IF NEW.birth_date IS DISTINCT FROM OLD.birth_date THEN
        UPDATE users SET birth_date = NEW.birth_date WHERE user_id = OLD.user_id;
    END IF;
    IF NEW.activo IS DISTINCT FROM OLD.activo THEN
        UPDATE estructura 
        SET activo = NEW.activo 
        WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.atril IS DISTINCT FROM OLD.atril THEN
        UPDATE estructura 
        SET atril = NEW.atril 
        WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.papel IS DISTINCT FROM OLD.papel THEN
        UPDATE estructura 
        SET papel_id = (SELECT papel_id FROM papeles WHERE papel = NEW.papel) 
        WHERE estructura_id = OLD.estructura_id 
        AND agrupacion_id = (SELECT agrupacion_id FROM agrupaciones WHERE agrupacion = OLD.agrupacion)
        AND seccion_id = (SELECT seccion_id FROM secciones WHERE seccion = OLD.seccion);
    END IF;
    IF NEW.agrupacion IS DISTINCT FROM OLD.agrupacion THEN
        UPDATE estructura 
        SET agrupacion_id = (SELECT agrupacion_id FROM agrupaciones WHERE agrupacion = NEW.agrupacion) 
        WHERE estructura_id = OLD.estructura_id 
        AND agrupacion_id = (SELECT agrupacion_id FROM agrupaciones WHERE agrupacion = OLD.agrupacion)
        AND seccion_id = (SELECT seccion_id FROM secciones WHERE seccion = OLD.seccion);
    END IF;
    IF NEW.seccion IS DISTINCT FROM OLD.seccion THEN
        UPDATE estructura 
        SET seccion_id = (SELECT seccion_id FROM secciones WHERE seccion = NEW.seccion) 
        WHERE estructura_id = OLD.estructura_id 
        AND agrupacion_id = (SELECT agrupacion_id FROM agrupaciones WHERE agrupacion = OLD.agrupacion)
        AND seccion_id = (SELECT seccion_id FROM secciones WHERE seccion = OLD.seccion);
    END IF;
    IF NEW.isla IS DISTINCT FROM OLD.isla THEN
        UPDATE residencia SET isla = NEW.isla WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.municipio IS DISTINCT FROM OLD.municipio THEN
        UPDATE residencia SET municipio = NEW.municipio WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.empadronamiento IS DISTINCT FROM OLD.empadronamiento THEN
        UPDATE residencia SET empadronamiento = NEW.empadronamiento WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.trabajo IS DISTINCT FROM OLD.trabajo THEN
        UPDATE empleos SET trabajo = NEW.trabajo WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.estudios IS DISTINCT FROM OLD.estudios THEN
        UPDATE empleos SET estudios = NEW.estudios WHERE estructura_id = OLD.estructura_id;
    END IF;
    IF NEW.matricula_number IS DISTINCT FROM OLD.matricula_number THEN
        UPDATE matriculas SET matricula_number = NEW.matricula_number WHERE estructura_id = OLD.estructura_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear el disparador update_all_data_trigger
CREATE TRIGGER update_all_data_trigger
INSTEAD OF UPDATE ON all_data
FOR EACH ROW
EXECUTE FUNCTION update_all_data();