import React, { useEffect, useRef, useState } from 'react'

import ReactDOM from 'react-dom/client'
import { useDispatch, useSelector } from 'react-redux'

import { NavLink, useSearchParams } from 'react-router-dom'

import { getCategories } from '../../features/categories/categoriesSlice'
import { getOrders, OrderRequest } from '../../features/orders/ordersSlice'
import { AppDispatch } from '../../features/store'
import styles from '../../styles/Orders.module.css'

export const Orders = ({ amount }: { amount: number }) => {
  const orders = useSelector(({ orders }) => orders)
  const categories = useSelector(({ categories }) => categories)

  const dispatch = useDispatch<AppDispatch>()

  const [searchParams] = useSearchParams()

  useEffect(() => {
    let req: OrderRequest = {
      categoryID: searchParams.get('category'),
      page: searchParams.get('page') ? searchParams.get('page') : '1',
      amount: searchParams.get('amount') ? searchParams.get('amount') : amount.toString(),
      status: 'open',
    }
    dispatch(getOrders(req))
    dispatch(getCategories())
  }, [dispatch, searchParams, amount])

  const showCategoriesList = () => {
    let list = document!.getElementById('categories_list')
    // @ts-ignore
    list.style.display = 'block'
  }

  const hideCategoriesList = () => {
    let list = document!.getElementById('categories_list')
    // @ts-ignore
    list.style.display = 'none'
  }

  // @ts-ignore
  const useOutsideCategories = (ref) => {
    useEffect(() => {
      // @ts-ignore
      function handleClickOutside(event) {
        if (ref.current && !ref.current.contains(event.target)) {
          hideCategoriesList()
        }
      }

      document.addEventListener('mousedown', handleClickOutside)
      return () => {
        document.removeEventListener('mousedown', handleClickOutside)
      }
    }, [ref])
  }

  const wrapperCategoriesRef = useRef(null)
  useOutsideCategories(wrapperCategoriesRef)

  const [selectedCategories, setSelectedCategories] = useState<number[]>([])

  const addCategory = (id: number, name: string) => {
    if (selectedCategories.includes(id)) {
      hideCategoriesList()
      return
    }

    const category_wrapper = document.createElement('div')
    document.getElementById('categories_box')?.append(category_wrapper)
    const category = (
      <div className={styles.selected_category} id={id.toString()}>
        {name}
      </div>
    )

    const wrap = ReactDOM.createRoot(category_wrapper)
    setSelectedCategories((selectedCategories) => [...selectedCategories, id])
    wrap.render(category)
    hideCategoriesList()
  }

  return (
    <div>
      <div className={styles.container}>
        <section className={styles.orders_container}>
          <div className={styles.header}>
            <h1>Заказы</h1>
          </div>
          <div className={styles.orders}>
            {orders.list.map(({ id, title, description }: { id: number; title: string; description: string }) => (
              <div key={id} className={styles.order}>
                <div className={styles.info}>
                  <NavLink to={`${id}`} className={styles.link}>
                    <h2 className={styles.order_title}>{title}</h2>
                  </NavLink>
                  <div className={styles.description}>{description}</div>
                </div>
              </div>
            ))}
          </div>
        </section>
        <section className={styles.config}>
          <div className={styles.config_categories}>
            <h3 className={styles.config_header}>Категория</h3>
            <div ref={wrapperCategoriesRef}>
              <div className={styles.select} onClick={showCategoriesList}>
                <input type='text' placeholder='Выберите категорию' className={styles.input} />
                <div className={styles.arrow}>
                  <svg width='16px' height='16px'>
                    <use xlinkHref={`${process.env.PUBLIC_URL}/sprite.svg#arrow`} />
                  </svg>
                </div>
              </div>
              <ul className={styles.categories_list} id='categories_list' style={{ display: 'none' }}>
                {categories.list.map(({ id, name }: { id: number; name: string }) => (
                  <li
                    key={id}
                    className={styles.category_option}
                    id={id.toString()}
                    onClick={() => addCategory(id, name)}
                  >
                    {name}
                  </li>
                ))}
              </ul>
              <div className={styles.categories_box} id='categories_box'></div>
            </div>
          </div>
          <div className={styles.config_food}>
            <h3 className={styles.config_header}>Способ оплаты</h3>
            <div className={styles.select}>
              <input type='text' placeholder='Выберите способ оплаты' className={styles.input} />
              <div className={styles.arrow}>
                <svg width='16px' height='16px'>
                  <use xlinkHref={`${process.env.PUBLIC_URL}/sprite.svg#arrow`} />
                </svg>
              </div>
            </div>
          </div>
          <div className={styles.config_confirm}>
            <button>Применить фильтры</button>
          </div>
        </section>
      </div>
    </div>
  )
}
