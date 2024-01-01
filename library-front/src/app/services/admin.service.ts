import { Injectable, inject } from '@angular/core';
import { AuthService } from './auth.service';
import { AdminOrder, Book, Customer, Order } from '../interfaces/entities';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BASE_URL } from 'src/utils/configs';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  authService: AuthService = inject(AuthService);
  orderList: AdminOrder[] = []

  constructor(private http: HttpClient) { }

  async getBookDetails(bookId: number): Promise<Book> {
    const getBookDetailsUrl = BASE_URL + 'admin/book/details/' + bookId;
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });
    
    let response = await this.http.get<any>(getBookDetailsUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
    const bookDetails: Book = {
      id: response.result.book_id,
      name: response.result.name,
      author: response.result.author,
      image: response.result.image !== undefined ? response.result.image : '',
      description: response.result.description,
      price: response.result.price,
      stock: response.result.stock,
      year: response.result.year,
      language: response.result.language
    };
    return bookDetails;
  }

  async getCustomerDetails(customerId: number): Promise<Customer> {
    const getCustomerDetailsUrl = BASE_URL + 'admin/customer/details/' + customerId;
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });
    
    let response = await this.http.get<any>(getCustomerDetailsUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
    const customerDetails: Customer = {
      id: response.result.user_id,
      name: response.result.name,
      email: response.result.email
    };
    return customerDetails;
  }

  async getOrders(): Promise<AdminOrder[]> {
    let getOrdersUrl = BASE_URL + 'admin/order/get/';
    
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

      let book: Book = await this.getBookDetails(order.book_id);
      let customer: Customer = await this.getCustomerDetails(order.customer_id);
      this.orderList.push({
        id: order.order_id,
        book: book,
        quantity: order.quantity,
        customer: customer,
        selected: false
      });
      
    }
    return this.orderList;
  }

  async removeOrder(orderId: number): Promise<void> {
    const removeOrderUrl = BASE_URL + 'admin/order/delete/' + orderId;
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });

    let response = await this.http.delete<any>(removeOrderUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
  }
}
