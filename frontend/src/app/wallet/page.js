"use client";

import { useState, useEffect } from "react";
import { getInfoAPI, sendCoinAPI } from "../../utils/api";
import PrivateRoute from "../../components/PrivateRoute";
import { useRouter } from "next/navigation";
import { AuthContext } from '../../context/AuthContext';
import { useContext } from "react";
import styles from './page.module.css';
import { ToastContainer, toast } from 'react-toastify';

export default function Wallet() {
  const { isAuthenticated } = useContext(AuthContext);
  const [balance, setBalance] = useState(0);
  const [inventory, setInventory] = useState([]);
  const [receivedHistory, setReceivedHistory] = useState([]);
  const [sentHistory, setSentHistory] = useState([]);
  const [amount, setAmount] = useState("");
  const [recipient, setRecipient] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sendError, setSendError] = useState("");
  const router = useRouter(); 

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login"); 
      return;
    }

    async function fetchData() {
      try {
        // Получаем информацию о балансе, инвентаре и истории монет
        const userInfo = await getInfoAPI();
        setBalance(userInfo.coins || 0);
        setInventory(userInfo.inventory || []);
        setReceivedHistory(userInfo.coinHistory?.received || []);
        setSentHistory(userInfo.coinHistory?.sent || []);
      } catch (error) {
        setError("Ошибка при загрузке данных.");
        console.error("Ошибка:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [router, isAuthenticated]);

  const handleSendCoins = async () => {
    setSendError("");

    if (!recipient || !amount) {
      toast.error("Пожалуйста, укажите получателя и сумму.");
      return;
    }

    if (parseFloat(amount) > balance) {
      toast.error("Сумма отправки не может превышать баланс.");
      return;
    }

    try {
      await sendCoinAPI(recipient, amount);
      toast.success("Монеты успешно отправлены!");
      setAmount("");
      setRecipient(""); 

      setBalance(prevBalance => prevBalance - parseFloat(amount));

      // Обновляем историю транзакций после отправки
      const userInfo = await getInfoAPI();
      setReceivedHistory(userInfo.coinHistory?.received || []);
      setSentHistory(userInfo.coinHistory?.sent || []);
    } catch (error) {
      toast.error(`Ошибка: ${error.message}`);
    }
  };

  return (
    <PrivateRoute>
      <div className={styles.wallet}>
        <h1 className={styles.wallet__title}>Кошелек</h1>
        {loading ? (
          <p className={styles.wallet__loading}>Загрузка...</p>
        ) : error ? (
          <p className={styles.wallet__loading}>{error}</p>
        ) : (
          <div className={styles.wallet__content}>
            <h2 className={styles.wallet__balance}>Баланс: {balance} монет</h2>

            <h3 className={styles.wallet__send_title}>Отправить монеты:</h3>
            <div className={styles.wallet__send_form}>
              <input
                type="text"
                className={styles.wallet__input}
                placeholder="Получатель"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
              />
              <input
                type="number"
                className={styles.wallet__input}
                placeholder="Сумма"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
              <button className={styles.wallet__button} onClick={handleSendCoins}>Отправить</button>
            </div>

            {receivedHistory.length === 0 ? (
              <p> </p>
            ) : (
              <>
              <h3 className={styles.wallet__transactions_title}>Получено:</h3>
              <ul className={styles.wallet__transactions_list}>
                {receivedHistory.map((transaction, index) => (
                  <li key={index} className={styles.wallet__transaction_item}>
                    <p>
                      {transaction.fromUser}<span>: </span> {transaction.amount} монет
                    </p>
                  </li>
                ))}
              </ul>
              </>
            )}

            {sentHistory.length === 0 ? (
              <p> </p>
            ) : (
              <>
              <h3 className={styles.wallet__transactions_title}>Отправлено:</h3>
              <ul className={styles.wallet__transactions_list}>
                {sentHistory.map((transaction, index) => (
                  <li key={index} className={styles.wallet__transaction_item}>
                    <p>
                      {transaction.toUser}<span>: </span> {transaction.amount} монет
                    </p>
                  </li>
                ))}
              </ul>
              </>
            )}
          </div>
        )}
        <ToastContainer /> 
      </div>
    </PrivateRoute>
  );
}
