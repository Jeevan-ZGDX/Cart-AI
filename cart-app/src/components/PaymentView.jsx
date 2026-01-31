import React, { useState } from 'react'
import axios from 'axios'
import { QRCodeSVG } from 'qrcode.react'
import './PaymentView.css'

const API_BASE = '/api/v1'

function PaymentView({ cartId, onPaymentComplete }) {
  const [qrData, setQrData] = useState(null)
  const [paymentMethod, setPaymentMethod] = useState('qr_code')
  const [processing, setProcessing] = useState(false)
  const [paymentResult, setPaymentResult] = useState(null)

  const generateQR = async () => {
    try {
      const response = await axios.post(`${API_BASE}/payment/${cartId}/qr`)
      setQrData(response.data)
    } catch (error) {
      console.error('Error generating QR:', error)
      alert('Failed to generate payment QR code')
    }
  }

  const processPayment = async () => {
    setProcessing(true)
    try {
      const response = await axios.post(`${API_BASE}/payment/process`, {
        cart_id: cartId,
        payment_method: paymentMethod
      })
      setPaymentResult(response.data)
      if (onPaymentComplete) {
        onPaymentComplete()
      }
    } catch (error) {
      console.error('Error processing payment:', error)
      alert('Payment failed')
    } finally {
      setProcessing(false)
    }
  }

  if (paymentResult) {
    return (
      <div className="payment-success">
        <h2>✅ Payment Successful!</h2>
        <div className="payment-details">
          <p><strong>Transaction ID:</strong> {paymentResult.transaction_id}</p>
          <p><strong>Amount:</strong> ${paymentResult.amount.toFixed(2)}</p>
          <p><strong>Payment Method:</strong> {paymentResult.payment_method}</p>
          <p><strong>Status:</strong> {paymentResult.status}</p>
        </div>
        {paymentResult.receipt_data && (
          <div className="receipt">
            <h3>Receipt</h3>
            <pre>{JSON.stringify(paymentResult.receipt_data, null, 2)}</pre>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="payment-view">
      <h2>Payment</h2>

      <div className="payment-method-selector">
        <label>
          <input
            type="radio"
            value="qr_code"
            checked={paymentMethod === 'qr_code'}
            onChange={(e) => setPaymentMethod(e.target.value)}
          />
          QR Code
        </label>
        <label>
          <input
            type="radio"
            value="nfc"
            checked={paymentMethod === 'nfc'}
            onChange={(e) => setPaymentMethod(e.target.value)}
          />
          NFC
        </label>
        <label>
          <input
            type="radio"
            value="card"
            checked={paymentMethod === 'card'}
            onChange={(e) => setPaymentMethod(e.target.value)}
          />
          Card
        </label>
        <label>
          <input
            type="radio"
            value="cash"
            checked={paymentMethod === 'cash'}
            onChange={(e) => setPaymentMethod(e.target.value)}
          />
          Cash
        </label>
      </div>

      {paymentMethod === 'qr_code' && (
        <div className="qr-section">
          <button onClick={generateQR} className="generate-qr-btn">
            Generate Payment QR Code
          </button>
          {qrData && (
            <div className="qr-display">
              <QRCodeSVG value={JSON.stringify({
                cart_id: cartId,
                amount: qrData.amount,
                reference: qrData.payment_reference
              })} size={256} />
              <p className="qr-amount">Amount: ${qrData.amount.toFixed(2)}</p>
              <p className="qr-reference">Ref: {qrData.payment_reference}</p>
            </div>
          )}
        </div>
      )}

      <div className="payment-actions">
        <button
          onClick={processPayment}
          className="process-payment-btn"
          disabled={processing}
        >
          {processing ? 'Processing...' : 'Complete Payment'}
        </button>
      </div>
    </div>
  )
}

export default PaymentView
