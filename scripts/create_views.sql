CREATE OR REPLACE VIEW top_selling_products AS
SELECT p.product_id, p.name, SUM(bi.quantity) AS total_quantity_sold, SUM(bi.subtotal) AS total_revenue
FROM products p JOIN bill_items bi ON p.product_id = bi.product_id
GROUP BY p.product_id, p.name ORDER BY total_quantity_sold DESC;

CREATE OR REPLACE VIEW most_profitable_products AS
SELECT p.product_id, p.name, SUM(bi.subtotal) - SUM(p.cost_price * bi.quantity) AS profit
FROM products p JOIN bill_items bi ON p.product_id = bi.product_id
GROUP BY p.product_id, p.name ORDER BY profit DESC;

CREATE OR REPLACE VIEW monthly_sales_summary AS
SELECT DATE_FORMAT(b.created_at, '%Y-%m') AS month, SUM(b.total_amount) AS total_sales, COUNT(DISTINCT b.bill_id) AS bills_count
FROM bills b GROUP BY month ORDER BY month DESC;
