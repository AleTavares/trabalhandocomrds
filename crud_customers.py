# import streamlit as st
# from crud import get_connection
# import psycopg2

# # Functions for CRUD operations on customers table

# def create_customer(customer):
#     conn = get_connection()
#     cur = conn.cursor()
#     sql = '''INSERT INTO customers (customer_id, company_name, contact_name, contact_title,
#                address, city, region, postal_code, country, phone, fax)
#              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
#     cur.execute(sql, (
#         customer['customer_id'], customer['company_name'], customer.get('contact_name'),
#         customer.get('contact_title'), customer.get('address'), customer.get('city'),
#         customer.get('region'), customer.get('postal_code'), customer.get('country'),
#         customer.get('phone'), customer.get('fax')
#     ))
#     conn.commit()
#     cur.close()
#     conn.close()


# def read_customers():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM customers ORDER BY customer_id')
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows


# def update_customer(customer_id, updated):
#     conn = get_connection()
#     cur = conn.cursor()
#     fields = []
#     values = []
#     for key, val in updated.items():
#         fields.append(f"{key} = %s")
#         values.append(val)
#     values.append(customer_id)
#     sql = f"UPDATE customers SET {', '.join(fields)} WHERE customer_id = %s"
#     cur.execute(sql, tuple(values))
#     conn.commit()
#     cur.close()
#     conn.close()


# def delete_customer(customer_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute('DELETE FROM customers WHERE customer_id = %s', (customer_id,))
#     conn.commit()
#     cur.close()
#     conn.close()

# # Streamlit UI
# st.title('CRUD de Customers')

# menu = ['Inserir', 'Visualizar', 'Atualizar', 'Deletar']
# choice = st.sidebar.selectbox('Menu', menu)

# if choice == 'Inserir':
#     st.subheader('Inserir Novo Customer')
#     with st.form('form_insert'):
#         cid = st.text_input('Customer ID (5 chars)')
#         company = st.text_input('Company Name')
#         contact = st.text_input('Contact Name')
#         title = st.text_input('Contact Title')
#         address = st.text_input('Address')
#         city = st.text_input('City')
#         region = st.text_input('Region')
#         postal = st.text_input('Postal Code')
#         country = st.text_input('Country')
#         phone = st.text_input('Phone')
#         fax = st.text_input('Fax')
#         submit = st.form_submit_button('Inserir')
#     if submit:
#         customer = {
#             'customer_id': cid,
#             'company_name': company,
#             'contact_name': contact,
#             'contact_title': title,
#             'address': address,
#             'city': city,
#             'region': region,
#             'postal_code': postal,
#             'country': country,
#             'phone': phone,
#             'fax': fax
#         }
#         create_customer(customer)
#         st.success('Customer inserido com sucesso!')

# elif choice == 'Visualizar':
#     st.subheader('Lista de Customers')
#     data = read_customers()
#     if data:
#         for row in data:
#             st.write(dict(
#                 customer_id=row[0], company_name=row[1], contact_name=row[2],
#                 contact_title=row[3], address=row[4], city=row[5], region=row[6],
#                 postal_code=row[7], country=row[8], phone=row[9], fax=row[10]
#             ))
#     else:
#         st.info('Nenhum customer encontrado.')

# elif choice == 'Atualizar':
#     st.subheader('Atualizar Customer')
#     cust_id = st.text_input('Customer ID a atualizar')
#     if cust_id:
#         with st.form('form_update'):
#             fields = {}
#             fields['company_name'] = st.text_input('Company Name')
#             fields['contact_name'] = st.text_input('Contact Name')
#             fields['contact_title'] = st.text_input('Contact Title')
#             fields['address'] = st.text_input('Address')
#             fields['city'] = st.text_input('City')
#             fields['region'] = st.text_input('Region')
#             fields['postal_code'] = st.text_input('Postal Code')
#             fields['country'] = st.text_input('Country')
#             fields['phone'] = st.text_input('Phone')
#             fields['fax'] = st.text_input('Fax')
#             upd = st.form_submit_button('Atualizar')
#         if upd:
#             # remove empty fields
#             updates = {k: v for k, v in fields.items() if v}
#             if updates:
#                 update_customer(cust_id, updates)
#                 st.success('Customer atualizado com sucesso!')
#             else:
#                 st.warning('Preencha ao menos um campo para atualizar.')

# elif choice == 'Deletar':
#     st.subheader('Deletar Customer')
#     cust_id_del = st.text_input('Customer ID a deletar')
#     if st.button('Deletar'):
#         if cust_id_del:
#             delete_customer(cust_id_del)
#             st.success('Customer deletado com sucesso!')
#         else:
#             st.warning('Informe o Customer ID para deletar.')