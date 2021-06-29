CREATE OR REPLACE FUNCTION add_to_pesanan()
RETURNS trigger AS
$$
	DECLARE
		shipping_address_id INTEGER;
	BEGIN
		SELECT a.customer_address_id  INTO shipping_address_id FROM "order" JOIN SHIPPING_ADDRESS a
		ON a.order_id = NEW.id;
		INSERT INTO PESANAN(status, customer_id, order_id, shipping_id, date_ordered) VALUES('PRO',NEW.customer_id, NEW.id, shipping_address_id, NEW.date_ordered);
		RETURN NEW;
	END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER add_new_order
AFTER INSERT OR UPDATE OF complete
ON "order"
FOR EACH ROW EXECUTE PROCEDURE add_to_pesanan();
