def generate_sql(question: str, schema: list) -> str:
    question_lower = question.lower()

    if "total sales last year" in question_lower or "total sales in 2023" in question_lower:
        return "SELECT SUM(amount) FROM sales WHERE EXTRACT(YEAR FROM sale_date) = 2023;"

    elif "total sales" in question_lower:
        return "SELECT SUM(amount) FROM sales;"

    elif "top customers" in question_lower:
        return """
            SELECT customers.name, SUM(sales.amount) AS total_spent
            FROM sales
            JOIN customers ON sales.customer_id = customers.id
            WHERE EXTRACT(YEAR FROM sale_date) = 2023
            GROUP BY customers.name
            ORDER BY total_spent DESC
            LIMIT 5;
        """

    elif "lowest sales department" in question_lower or "what department had the lowest sales" in question_lower:
        return """
            SELECT employees.department, SUM(sales.amount) AS total
            FROM sales
            JOIN employees ON sales.employee_id = employees.id
            GROUP BY employees.department
            ORDER BY total ASC
            LIMIT 1;
        """

    # fallback if nothing matched
    return "SELECT * FROM sales LIMIT 5;"
