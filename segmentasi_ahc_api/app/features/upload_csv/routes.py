import io
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

from segmentasi_ahc_api.app.database import SessionDep
from segmentasi_ahc_api.app.features.upload_csv.utils import get_or_create_customer, get_or_create_product
from segmentasi_ahc_api.app.models.transactions import Transaction, TransactionItem

upload_csv_router = APIRouter(prefix='/upload_csv', tags=['upload_csv'])


@upload_csv_router.post("/")
async def upload_csv(
        db: SessionDep,
        file: UploadFile = File(...)
) -> dict:
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    contents = await file.read()
    try:
        # Membaca CSV ke pandas dataframe
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Loop untuk setiap baris di CSV
        for _, row in df.iterrows():
            # Ambil atau buat customer
            customer = get_or_create_customer(db, row['nama_customer'])

            # Ambil atau buat produk
            product = get_or_create_product(db, row['nama_barang'], row['kategori'], row['size'], row['harga_satuan'])

            # Buat transaksi baru
            transaction = Transaction(
                customer_id=customer.id,
                transaction_date=datetime.strptime(row['tanggal'], "%Y-%m-%d %H:%M:%S").date(),
                total_amount=row['total_pembayaran']
            )
            db.add(transaction)
            db.commit()
            db.refresh(transaction)

            # Tambahkan item transaksi
            transaction_item = TransactionItem(
                transaction_id=transaction.id,
                product_id=product.id,
                quantity=row['jumlah_barang'],
                unit_price=row['harga_satuan'],
                total_price=row['total_pembayaran']
            )
            db.add(transaction_item)

        # Commit setelah semua data berhasil ditambahkan
        db.commit()

        return {"filename": file.filename, "status": "success", "row_count": len(df)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")
