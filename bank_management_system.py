# bank managment system 
# class account
# class bank
# class bankgui

import random
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib

# class account dy toll account deatails ba pa dy class kee yee
class Account:
    def __init__(self, account_id, name, password, balance=0):
        self.account_id = account_id
        self.name = name
        self.password = password
        self.balance = balance

# deposit function dy che sa money mong da yew account na bal account ta laygu
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: Rs{self.balance}"
        return "Invalid deposit amount."

# da withdraw functiion dy che sa rupay mong da account na rawobasoo
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: Rs{self.balance}"
        else:
            return "Insufficient funds or invalid amount."

# balance function dy che da balance check kee
    def check_balance(self):
        return f"Current balance: Rs{self.balance}"

# aww money transfer kawalo function dy
    def transfer(self, recipient, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            return f"Transferred Rs{amount} to {recipient.name}. Your new balance: Rs{self.balance}"
        return "Transfer failed: Insufficient funds or invalid amount."

# class bank dy
class Bank:
    def __init__(self):
        self.conn = sqlite3.connect('bank.db')
        self.cursor = self.conn.cursor()
        # Create accounts table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0
        )''')
        # Create transactions table for logging
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            recipient_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id)
        )''')
        self.conn.commit()

# da function ba mong account joree
    def create_account(self, account_id, name, password):
        if not account_id or not name or not password:
            return "All fields are required."
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO accounts (account_id, name, password) VALUES (?, ?, ?)", (account_id, name, hashed_password))
            self.conn.commit()
            return f"Account created! ID: {account_id}"
        except sqlite3.IntegrityError:
            return "Account ID already exists. Please choose a different ID."

# aww da login function dy che sok account ta login kee geee
    def login(self, account_id, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM accounts WHERE account_id = ? AND password = ?", (account_id, hashed_password))
        row = self.cursor.fetchone()
        if row:
            account_id, name, password, balance = row
            return Account(account_id, name, password, balance)
        return None

    def get_account(self, account_id):
        self.cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
        row = self.cursor.fetchone()
        if row:
            account_id, name, password, balance = row
            return Account(account_id, name, password, balance)
        return None

    def update_balance(self, account_id, new_balance):
        self.cursor.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (new_balance, account_id))
        self.conn.commit()

    def log_transaction(self, account_id, transaction_type, amount, recipient_id=None):
        self.cursor.execute("INSERT INTO transactions (account_id, type, amount, recipient_id) VALUES (?, ?, ?, ?)", (account_id, transaction_type, amount, recipient_id))
        self.conn.commit()

    def get_transaction_history(self, account_id):
        self.cursor.execute("SELECT type, amount, recipient_id, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp DESC", (account_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# da zamong sara da graphical user interface class dy
class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 JAAD BANK Management System")
        self.root.geometry("600x500")
        self.root.configure(bg="#0d47a1")
        self.root.resizable(True, True)
        self.fullscreen = False
        self.bank = Bank()
        self.current_user = None

        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.header_frame = tk.Frame(root, bg="#1565C0", height=60)
        self.header_frame.pack(fill="x", side="top")
        tk.Label(self.header_frame, text="🏦 JAAD Bank Management System", font=("Arial", 18, "bold"), bg="#1565C0", fg="white").pack(pady=10)

        self.main_frame = tk.Frame(root, bg="#0d47a1")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.login_frame = tk.Frame(self.main_frame, bg="#0d47a1")
        self.create_login_ui()

        self.account_frame = tk.Frame(self.main_frame, bg="#0d47a1")

        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Please login or create an account")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", bg="#0d47a1", fg="white", font=("Arial", 9))
        self.status_bar.pack(side="bottom", fill="x")

        self.show_login()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        if not self.fullscreen:
            self.root.geometry("600x500")

    def exit_fullscreen(self, event=None):
        if self.fullscreen:
            self.toggle_fullscreen()

    def create_login_ui(self):
        title_label = tk.Label(self.login_frame, text="🌟 Welcome to Your JAAD Banking Portal", font=("Arial", 16, "bold"), bg="#0d47a1", fg="#BBDEFB")
        title_label.pack(pady=(0, 20))

        create_frame = tk.LabelFrame(self.login_frame, text="📝 Create New Account", bg="#0d47a1", fg="#BBDEFB", font=("Arial", 12, "bold"), padx=20, pady=10)
        create_frame.pack(fill="x", pady=(0, 20))

        tk.Label(create_frame, text="Account ID:", bg="#0d47a1", fg="white", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.account_id_entry = tk.Entry(create_frame, width=35, font=("Arial", 10))
        self.account_id_entry.grid(row=0, column=1, pady=8, padx=(10, 0))

        tk.Label(create_frame, text="Full Name:", bg="#0d47a1", fg="white", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.name_entry = tk.Entry(create_frame, width=35, font=("Arial", 10))
        self.name_entry.grid(row=1, column=1, pady=8, padx=(10, 0))

        tk.Label(create_frame, text="Password:", bg="#0d47a1", fg="white", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=8)
        self.pass_entry = tk.Entry(create_frame, show="*", width=35, font=("Arial", 10))
        self.pass_entry.grid(row=2, column=1, pady=8, padx=(10, 0))

        create_btn = tk.Button(create_frame, text="✨ Create Account", command=self.create_account, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5)
        create_btn.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Frame(self.login_frame, height=2, bg="#BBDEFB").pack(fill="x", pady=10)

        login_frame = tk.LabelFrame(self.login_frame, text="🔐 Login to Your Account", bg="#0d47a1", fg="#BBDEFB", font=("Arial", 12, "bold"), padx=20, pady=10)
        login_frame.pack(fill="x", pady=(0, 20))

        tk.Label(login_frame, text="Account ID:", bg="#0d47a1", fg="white", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.id_entry = tk.Entry(login_frame, width=35, font=("Arial", 10))
        self.id_entry.grid(row=0, column=1, pady=8, padx=(10, 0))

        tk.Label(login_frame, text="Password:", bg="#0d47a1", fg="white", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.login_pass_entry = tk.Entry(login_frame, show="*", width=35, font=("Arial", 10))
        self.login_pass_entry.grid(row=1, column=1, pady=8, padx=(10, 0))

        login_btn = tk.Button(login_frame, text="🚀 Login", command=self.login, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5)
        login_btn.grid(row=2, column=0, columnspan=2, pady=15)

        exit_btn = tk.Button(self.login_frame, text="❌ Exit Application", command=self.exit_app, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5)
        exit_btn.pack(pady=10)

    def create_account_ui(self):
        welcome_label = tk.Label(self.account_frame, text=f"👋 Welcome back, {self.current_user.name}!", font=("Arial", 16, "bold"), bg="#0d47a1", fg="#4CAF50")
        welcome_label.pack(pady=(0, 20))

        info_frame = tk.LabelFrame(self.account_frame, text="📊 Account Overview", bg="#0d47a1", fg="#BBDEFB", font=("Arial", 12, "bold"), padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 20))
        tk.Label(info_frame, text=f"🆔 Account ID: {self.current_user.account_id}", bg="#0d47a1", fg="white", font=("Arial", 11)).pack(anchor="w", pady=5)
        self.balance_label = tk.Label(info_frame, text=f"💵 Balance: Rs{self.current_user.balance}", bg="#0d47a1", fg="white", font=("Arial", 11))
        self.balance_label.pack(anchor="w", pady=5)

        buttons_frame = tk.Frame(self.account_frame, bg="#0d47a1")
        buttons_frame.pack()

        deposit_btn = tk.Button(buttons_frame, text="💰 Deposit Funds", command=self.deposit, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15, pady=8)
        deposit_btn.grid(row=0, column=0, padx=15, pady=10)

        withdraw_btn = tk.Button(buttons_frame, text="💸 Withdraw Funds", command=self.withdraw, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15, pady=8)
        withdraw_btn.grid(row=0, column=1, padx=15, pady=10)

        balance_btn = tk.Button(buttons_frame, text="📊 Check Balance", command=self.check_balance, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15, pady=8)
        balance_btn.grid(row=1, column=0, padx=15, pady=10)

        transfer_btn = tk.Button(buttons_frame, text="🔄 Transfer Money", command=self.transfer, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15, pady=8)
        transfer_btn.grid(row=1, column=1, padx=15, pady=10)

        history_btn = tk.Button(buttons_frame, text="📜 Transaction History", command=self.show_history, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15, pady=8)
        history_btn.grid(row=2, column=0, padx=15, pady=10)

        logout_btn = tk.Button(self.account_frame, text="🔓 Logout", command=self.logout, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5)
        logout_btn.pack(pady=20)

    def update_balance_display(self):
        if self.current_user and hasattr(self, 'balance_label'):
            self.balance_label.config(text=f"💵 Balance: Rs{self.current_user.balance}")

    def show_login(self):
        self.account_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
        self.status_var.set("Ready - Please login or create an account")

    def show_account(self):
        self.login_frame.pack_forget()
        self.account_frame.pack(fill="both", expand=True)
        self.status_var.set(f"Logged in as {self.current_user.name}")

    def create_account(self):
        account_id = self.account_id_entry.get().strip()
        name = self.name_entry.get().strip()
        password = self.pass_entry.get().strip()
        if account_id and name and password:
            message = self.bank.create_account(account_id, name, password)
            if "created" in message:
                messagebox.showinfo("Success", message)
                self.account_id_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.pass_entry.delete(0, tk.END)
                self.status_var.set("Account created successfully")
            else:
                messagebox.showerror("Error", message)
                self.status_var.set("Account creation failed")
        else:
            messagebox.showerror("Error", "Please fill all fields.")
            self.status_var.set("Error: Missing fields")

    def login(self):
        account_id = self.id_entry.get().strip()
        password = self.login_pass_entry.get().strip()
        user = self.bank.login(account_id, password)
        if user:
            self.current_user = user
            self.create_account_ui()
            self.show_account()
            self.id_entry.delete(0, tk.END)
            self.login_pass_entry.delete(0, tk.END)
            self.status_var.set(f"Logged in as {self.current_user.name}")
        else:
            messagebox.showerror("Error", "Invalid credentials.")
            self.status_var.set("Login failed")

    def deposit(self):
        amount = self.get_amount("Deposit Amount")
        if amount is not None:
            message = self.current_user.deposit(amount)
            self.bank.update_balance(self.current_user.account_id, self.current_user.balance)
            self.bank.log_transaction(self.current_user.account_id, "Deposit", amount)
            messagebox.showinfo("Deposit", message)
            self.update_balance_display()
            self.status_var.set("Deposit completed")

    def withdraw(self):
        amount = self.get_amount("Withdraw Amount")
        if amount is not None:
            message = self.current_user.withdraw(amount)
            if "Withdrew" in message:
                self.bank.update_balance(self.current_user.account_id, self.current_user.balance)
                self.bank.log_transaction(self.current_user.account_id, "Withdraw", amount)
                messagebox.showinfo("Withdraw", message)
                self.update_balance_display()
                self.status_var.set("Withdrawal completed")
            else:
                messagebox.showerror("Error", message)
                self.status_var.set("Withdrawal failed")

    def check_balance(self):
        message = self.current_user.check_balance()
        messagebox.showinfo("Balance", message)
        self.status_var.set("Balance checked")

    def transfer(self):
        recipient_id = self.get_input("Recipient Account ID")
        if recipient_id:
            recipient = self.bank.get_account(recipient_id)
            if recipient:
                amount = self.get_amount("Transfer Amount")
                if amount is not None:
                    message = self.current_user.transfer(recipient, amount)
                    if "Transferred" in message:
                        self.bank.update_balance(self.current_user.account_id, self.current_user.balance)
                        self.bank.update_balance(recipient.account_id, recipient.balance)
                        self.bank.log_transaction(self.current_user.account_id, "Transfer", amount, recipient_id)
                        self.bank.log_transaction(recipient.account_id, "Receive", amount, self.current_user.account_id)
                        messagebox.showinfo("Transfer", message)
                        self.update_balance_display()
                        self.status_var.set("Transfer completed")
                    else:
                        messagebox.showerror("Error", message)
                        self.status_var.set("Transfer failed")
            else:
                messagebox.showerror("Error", "Recipient account not found.")
                self.status_var.set("Transfer failed: Account not found")

    def show_history(self):
        history = self.bank.get_transaction_history(self.current_user.account_id)
        if not history:
            messagebox.showinfo("History", "No transactions found.")
            return
        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        history_window.geometry("500x400")
        history_window.configure(bg="#0d47a1")

        tree = ttk.Treeview(history_window, columns=("Type", "Amount", "Recipient", "Timestamp"), show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Recipient", text="Recipient")
        tree.heading("Timestamp", text="Timestamp")
        tree.pack(fill="both", expand=True)

        for trans in history:
            tree.insert("", "end", values=trans)

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            self.current_user = None
            self.account_frame.pack_forget()
            self.show_login()
            self.status_var.set("Logged out successfully")

    def exit_app(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit the application?")
        if confirm:
            self.bank.close()
            self.root.destroy()

    def get_input(self, prompt):
        """Show a popup window asking for user input and return the entered text."""
        input_window = tk.Toplevel(self.root)
        input_window.title(prompt)
        input_window.geometry("300x150")
        input_window.configure(bg="#0d47a1")
        input_window.resizable(False, False)

        tk.Label(
            input_window,
            text=prompt,
            bg="#0d47a1",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        entry = tk.Entry(input_window, font=("Arial", 10))
        entry.pack(pady=5)
        entry.focus()

        result = {"value": None}

        def confirm():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("Error", "Input cannot be empty.")
                return
            result["value"] = value
            input_window.destroy()

        tk.Button(
            input_window,
            text="OK",
            command=confirm,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat"
        ).pack(pady=10)

        input_window.grab_set()
        self.root.wait_window(input_window)
        return result["value"]

    def get_amount(self, prompt):
        """Get a valid numeric amount from the user."""
        amount_str = self.get_input(prompt)
        if amount_str:
            try:
                amount = float(amount_str)
                if amount > 0:
                    return amount
                else:
                    messagebox.showerror("Error", "Amount must be greater than zero.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
        return None

    def deposit(self):
        amount = self.get_amount("Enter deposit amount")
        if amount is not None:
            message = self.current_user.deposit(amount)
            self.bank.update_balance(self.current_user.account_id, self.current_user.balance)
            self.bank.log_transaction(self.current_user.account_id, "Deposit", amount)
            self.update_balance_display()
            messagebox.showinfo("Deposit Successful", message)
            self.status_var.set("Deposit completed successfully.")

    def withdraw(self):
        amount = self.get_amount("Enter withdrawal amount")
        if amount is not None:
            message = self.current_user.withdraw(amount)
            if "Withdrew" in message:
                self.bank.update_balance(self.current_user.account_id, self.current_user.balance)
                self.bank.log_transaction(self.current_user.account_id, "Withdraw", amount)
                self.update_balance_display()
                messagebox.showinfo("Withdrawal Successful", message)
                self.status_var.set("Withdrawal completed successfully.")
            else:
                messagebox.showerror("Error", message)
                self.status_var.set("Withdrawal failed.")

    def transfer(self):
        recipient_id = self.get_input("Enter recipient Account ID")
        if recipient_id:
            recipient = self.bank.get_account(recipient_id)
            if not recipient:
                messagebox.showerror("Error", "Recipient account not found.")
                return
            amount = self.get_amount("Enter transfer amount")
            if amount is not None:
                message = self.current_user.transfer(recipient, amount)
                if "Transferred" in message:
                    self.bank.update_balance(self.current_user.account_id, self.current_user.balance)
                    self.bank.update_balance(recipient.account_id, recipient.balance)
                    self.bank.log_transaction(self.current_user.account_id, "Transfer", amount, recipient_id)
                    self.bank.log_transaction(recipient.account_id, "Receive", amount, self.current_user.account_id)
                    self.update_balance_display()
                    messagebox.showinfo("Transfer Successful", message)
                    self.status_var.set("Transfer completed successfully.")
                else:
                    messagebox.showerror("Error", message)
                    self.status_var.set("Transfer failed.")

# -------------------------------
# Main program entry point
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()
