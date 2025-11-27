-- AI Agent Database Schema
-- Inicializační skript pro SQLite databázi

-- Vytvoření tabulky produktů
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Vytvoření tabulky pro logování dotazů
CREATE TABLE IF NOT EXISTS query_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    execution_time REAL
);

-- Vložení ukázkových dat - Elektronika
INSERT INTO products (name, category, price, stock, description) VALUES
    ('Notebook Dell XPS 13', 'Elektronika', 29990, 5, 'Výkonný ultrabook s Intel i7, 16GB RAM, 512GB SSD'),
    ('iPhone 15 Pro', 'Elektronika', 34990, 8, 'Nejnovější iPhone s titaniovým rámem a USB-C'),
    ('Samsung Galaxy S24', 'Elektronika', 24990, 12, 'Prémiový Android smartphone s AI funkcemi'),
    ('Sony WH-1000XM5', 'Elektronika', 9990, 15, 'Bezdrátová sluchátka s aktivním potlačením hluku'),
    ('iPad Pro 12.9"', 'Elektronika', 35990, 6, 'Profesionální tablet s M2 chipem'),
    ('Apple Watch Series 9', 'Elektronika', 12990, 10, 'Chytré hodinky s pokročilým zdravotním monitoringem');

-- Vložení ukázkových dat - Oblečení
INSERT INTO products (name, category, price, stock, description) VALUES
    ('Pánská zimní bunda North Face', 'Oblečení', 5990, 20, 'Zateplená nepromokavá bunda'),
    ('Dámské běžecké boty Nike Air Zoom', 'Oblečení', 3490, 25, 'Lehké běžecké boty s odpružením'),
    ('Unisex mikina Adidas', 'Oblečení', 1490, 30, 'Bavlněná mikina s kapucí'),
    ('Pánské džíny Levi\'s 501', 'Oblečení', 2490, 18, 'Klasické džíny straight fit');

-- Vložení ukázkových dat - Potraviny
INSERT INTO products (name, category, price, stock, description) VALUES
    ('Bio káva z Etiopie', 'Potraviny', 249, 50, 'Zrnková káva arabica, 250g'),
    ('Organický med', 'Potraviny', 189, 40, 'Lesní med od českých včelařů, 500g'),
    ('Extra panenský olivový olej', 'Potraviny', 299, 35, 'Řecký olivový olej, 500ml'),
    ('Čokoláda Lindt 85%', 'Potraviny', 59, 100, 'Hořká čokoláda Excellence, 100g');

-- Vložení ukázkových dat - Domácnost
INSERT INTO products (name, category, price, stock, description) VALUES
    ('Dyson V15 vysavač', 'Domácnost', 18990, 7, 'Bezdrátový tyčový vysavač s laserem'),
    ('Philips Airfryer XXL', 'Domácnost', 7990, 12, 'Fritéza na horký vzduch, 7.3L'),
    ('Robot vysavač iRobot Roomba', 'Domácnost', 12990, 9, 'Automatický vysavač s mapováním');

-- Vytvoření indexů pro optimalizaci dotazů
CREATE INDEX IF NOT EXISTS idx_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_stock ON products(stock);
CREATE INDEX IF NOT EXISTS idx_query_timestamp ON query_log(timestamp);

-- Vytvoření view pro statistiky
CREATE VIEW IF NOT EXISTS product_statistics AS
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price,
    SUM(stock) as total_stock,
    SUM(price * stock) as total_value
FROM products
GROUP BY category;

-- Vytvoření view pro nejprodávanější produkty (simulace)
CREATE VIEW IF NOT EXISTS popular_products AS
SELECT 
    id,
    name,
    category,
    price,
    stock,
    description,
    CASE 
        WHEN stock < 10 THEN 'Vysoká poptávka'
        WHEN stock < 20 THEN 'Střední poptávka'
        ELSE 'Dostupné'
    END as popularity
FROM products
ORDER BY stock ASC;

-- Trigger pro automatické logování změn v produktech
CREATE TRIGGER IF NOT EXISTS log_product_changes
AFTER UPDATE ON products
BEGIN
    INSERT INTO query_log (question, response, timestamp)
    VALUES (
        'Auto-log: Produkt aktualizován',
        'ID: ' || NEW.id || ', Název: ' || NEW.name || ', Nový sklad: ' || NEW.stock,
        datetime('now')
    );
END;

-- Výpis základních statistik
SELECT 'Databáze úspěšně inicializována!' as status;
SELECT 
    COUNT(*) as total_products,
    COUNT(DISTINCT category) as categories,
    ROUND(AVG(price), 2) as avg_price,
    SUM(stock) as total_stock_items
FROM products;
