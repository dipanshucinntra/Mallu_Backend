DELIMITER //
CREATE PROCEDURE `get_bp_details`(From_Date varchar(30), To_Date varchar(30), card_code varchar(30), ship_to_code varchar(30), final_status varchar(30))
	BEGIN
		IF (From_Date = '' AND  To_Date = '') THEN
				SELECT Order_order.id, Order_order.CardName AS Customer, Order_order.CreationDate AS PostingDate, Order_order.DocTotal AS TotalAmount, Order_order.FinalStatus AS ApprovalStatus, Order_order.DocumentStatus, Order_order.DiscountPercent AS Discount, Order_order.PayToCode AS BillToAddress, order_order.ShipToCode AS ShipToAddress, order_order.Comments FROM Order_order
                WHERE Order_order.CreateDate AND CardCode=card_code AND ShipToCode=ship_to_code AND final_status=final_status;
        ELSEIF (card_code ='') THEN
				SELECT Order_order.id, Order_order.CardName AS Customer, Order_order.CreationDate AS PostingDate, Order_order.DocTotal AS TotalAmount, Order_order.FinalStatus AS ApprovalStatus, Order_order.DocumentStatus, Order_order.DiscountPercent AS Discount, Order_order.PayToCode AS BillToAddress, order_order.ShipToCode AS ShipToAddress, order_order.Comments FROM Order_order
                WHERE Order_order.CreateDate BETWEEN From_Date AND To_Date AND ShipToCode=ship_to_code AND final_status=final_status;
        ELSEIF (ship_to_code = '') THEN
				SELECT Order_order.id, Order_order.CardName AS Customer, Order_order.CreationDate AS PostingDate, Order_order.DocTotal AS TotalAmount, Order_order.FinalStatus AS ApprovalStatus, Order_order.DocumentStatus, Order_order.DiscountPercent AS Discount, Order_order.PayToCode AS BillToAddress, order_order.ShipToCode AS ShipToAddress, order_order.Comments FROM Order_order
                WHERE Order_order.CreateDate BETWEEN From_Date AND To_Date AND CardCode=card_code AND final_status=final_status;
        ELSEIF (final_status = '' ) THEN
				SELECT Order_order.id, Order_order.CardName AS Customer, Order_order.CreationDate AS PostingDate, Order_order.DocTotal AS TotalAmount, Order_order.FinalStatus AS ApprovalStatus, Order_order.DocumentStatus, Order_order.DiscountPercent AS Discount, Order_order.PayToCode AS BillToAddress, order_order.ShipToCode AS ShipToAddress, order_order.Comments FROM Order_order
                WHERE Order_order.CreateDate BETWEEN From_Date AND To_Date AND CardCode=card_code AND ShipToCode=ship_to_code;
        ELSEIF (From_Date = ''  AND To_Date = '' AND card_code ='' AND ship_to_code ='' AND final_status = '') THEN
				SELECT Order_order.id, Order_order.CardName AS Customer, Order_order.CreationDate AS PostingDate, Order_order.DocTotal AS TotalAmount, Order_order.FinalStatus AS ApprovalStatus, Order_order.DocumentStatus, Order_order.DiscountPercent AS Discount, Order_order.PayToCode AS BillToAddress, order_order.ShipToCode AS ShipToAddress, order_order.Comments FROM Order_order;
        ELSE 
				SELECT Order_order.id, Order_order.CardName AS Customer, Order_order.CreationDate AS PostingDate, Order_order.DocTotal AS TotalAmount, Order_order.FinalStatus AS ApprovalStatus, Order_order.DocumentStatus, Order_order.DiscountPercent AS Discount, Order_order.PayToCode AS BillToAddress, order_order.ShipToCode AS ShipToAddress, order_order.Comments FROM Order_order
                WHERE Order_order.CreateDate BETWEEN From_Date AND To_Date AND CardCode=card_code AND ShipToCode=ship_to_code AND final_status=final_status;
		END IF; 
	END//
DELIMITER ;