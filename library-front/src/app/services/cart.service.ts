import { Injectable, inject } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Book, Order } from '../interfaces/entities';
import { BASE_URL } from 'src/utils/configs';
import { CreateOrderRequest } from '../interfaces/requests';
import { OrderListResponse } from '../interfaces/responses';
import { BookService } from './book.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {

  authService: AuthService = inject(AuthService);
  bookService: BookService = inject(BookService);
  constructor(private http: HttpClient) { }
  orderList: Order[] = []

  async addToCart(bookId: number, quantity: number): Promise<void> {
    const addToCartUrl = BASE_URL + 'manager/order/create/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString()
    });

    const requestBody: CreateOrderRequest = {
      book_id: bookId,
      quantity: quantity
    };

    let response = await this.http.post<any>(addToCartUrl, requestBody, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
  }
  async getOrders(purchased: boolean): Promise<Order[]> {
    let getOrdersUrl = BASE_URL + 'manager/order/get/';
    
    if(purchased)
    {
      getOrdersUrl = BASE_URL + 'manager/payment/buy/get/';
    }
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });

    let response = await this.http.get<any>(getOrdersUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
    this.orderList = [];
    for(const order of response.result.order_list)
    {

      let book: Book = await this.bookService.getBookDetails(order.book_id);
      this.orderList.push({
        id: order.order_id,
        book: book,
        quantity: order.quantity,
        selected: false
      });
      
    }
    return this.orderList;
  }

  async removeOrder(orderId: number): Promise<void> {
    const removeOrderUrl = BASE_URL + 'manager/order/delete/' + orderId;
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });

    let response = await this.http.delete<any>(removeOrderUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
  }

  async buyOrder(orderId: number): Promise<void> {
    const buyOrderUrl = BASE_URL + 'manager/payment/buy/' + orderId;
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });

    
    let response = await this.http.post<any>(buyOrderUrl, {}, { headers: headers }).toPromise();

    await this.authService.handleResponse(response);
  }


}
