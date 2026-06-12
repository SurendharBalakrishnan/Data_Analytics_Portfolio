CREATE TABLE [dbo].[finance_transactions] (

	[transaction_id] varchar(8000) NULL, 
	[transaction_date] date NULL, 
	[account_id] varchar(8000) NULL, 
	[customer_id] varchar(8000) NULL, 
	[transaction_type] varchar(8000) NULL, 
	[channel] varchar(8000) NULL, 
	[merchant_category] varchar(8000) NULL, 
	[fee_amount] float NULL, 
	[tax_amount] float NULL, 
	[currency] varchar(8000) NULL, 
	[transaction_status] varchar(8000) NULL, 
	[is_fraud] varchar(8000) NULL, 
	[risk_score] bigint NULL, 
	[reference_no] varchar(8000) NULL, 
	[amount] float NULL
);