
-- View: top_selling_products (by quantity)
CREATE OR REPLACE VIEW top_selling_products AS
SELECT p.product_id, p.name, SUM(bi.quantity) AS total_sold
FROM products p
JOIN bill_items bi ON p.product_id = bi.product_id
GROUP BY p.product_id, p.name
ORDER BY total_sold DESC;

-- View: most_profitable_products (profit = (price - cost_price) * qty)
CREATE OR REPLACE VIEW most_profitable_products AS
SELECT p.product_id, p.name, SUM((p.price - COALESCE(p.cost_price,0))*bi.quantity) AS profit
FROM products p
JOIN bill_items bi ON p.product_id = bi.product_id
GROUP BY p.product_id, p.name
ORDER BY profit DESC;
