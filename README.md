# Odoo Sales Credit Limit & Approval Workflow

This professional Odoo module extends the standard Sales functionality by introducing a robust **Credit Limit Control** and a dedicated **Approval Process**. It ensures financial security by preventing sales to customers who have exceeded their pre-defined credit thresholds.

## 🚀 Key Features

* **Customer Credit Management**: Set individual credit limits for each customer directly on their profile.
* **Automated Validation**: The system automatically checks the total outstanding balance + current order total during confirmation.
* **Blocking Mechanism**: Prevents the confirmation of Sales Orders if the credit limit is exceeded.
* **Approval Workflow**: Automatically generates an "Approval Request" when a limit is breached, allowing authorized managers to review and approve/reject the sale.
* **Dedicated Dashboard**: A centralized view for managers to track and process all pending approval requests.

## 🛠 Technical Stack

* **Backend**: Python (Odoo Framework)
* **Frontend**: Odoo XML (QWeb)
* **Database**: PostgreSQL
* **Concurrency Handling**: Integrated `cr.commit()` logic for reliable request logging during validation errors.

## 📂 Module Structure

- `models/`: Contains the logic for Sales Order extensions, Credit Limit settings, and Approval Request entities.
- `views/`: Custom UI forms, list views, and menu actions for the approval workflow.
- `security/`: Access Rights (ACL) ensuring only authorized personnel can approve requests.

## ⚙️ Installation

1. Copy the `my_credit_module` folder to your Odoo `custom_addons` directory.
2. Update your `odoo.conf` to include the custom addons path.
3. Restart the Odoo server.
4. Enable the module from the Apps menu.

---
*Developed as a technical task for Odoo development mastery.*
