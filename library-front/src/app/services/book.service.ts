import { Injectable, inject } from '@angular/core';
import {Book} from '../interfaces/entities'
import { AuthService } from './auth.service';
import { BASE_URL } from 'src/utils/configs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BookListResponse } from '../interfaces/responses';
import { CreateBookRequest, UpdateBookRequest } from '../interfaces/requests';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  authService: AuthService = inject(AuthService);
  constructor(private http: HttpClient) { }
  bookList: Book[] = []

  async getBooks(): Promise<Book[]> {
    const getBooksUrl = BASE_URL + 'manager/book/get/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });
    

    const role = this.authService.getRole();
    let response = await this.http.get<any>(getBooksUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
    this.bookList = response.result.book_list.map((b: BookListResponse) => ({
      id: b.book_id,
      name: b.name,
      author: b.author,
      image: b.image,
      price: b.price,
      year: b.year,
      language: b.language
    }));
    
    return this.bookList
  }

  async getBookDetails(bookId: number): Promise<Book> {
    const getBookDetailsUrl = BASE_URL + 'manager/book/search/' + bookId;
    
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

  async createBook(name: String, author: String, stock: number, description: String, price: number, year: String, language: String): Promise<void> {
    const createBookUrl = BASE_URL + 'manager/book/create/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });
    
    const requestBody: CreateBookRequest = {
      name: name,
      author: author,
      stock: stock,
      description: description,
      price: price,
      year: year,
      language: language
    };

    let response = await this.http.post<any>(createBookUrl, requestBody, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
  }

  async updateBook(bookId: number, name: String, author: String, stock: number, description: String, price: number, year: String, language: String): Promise<void> {
    const updateBookUrl = BASE_URL + 'manager/book/update/';
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });
    
    const requestBody: UpdateBookRequest = {
      book_id: bookId,
      name: name,
      author: author,
      stock: stock,
      description: description,
      price: price,
      year: year,
      language: language
    };

    let response = await this.http.post<any>(updateBookUrl, requestBody, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
  }

  async deleteBook(bookId: number): Promise<void> {
    const deleteBookUrl = BASE_URL + 'manager/book/delete/' + bookId;
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Token': this.authService.getAccessToken().toString(),
      'lang': 'en'
    });
    

    let response = await this.http.delete<any>(deleteBookUrl, { headers: headers }).toPromise();
    await this.authService.handleResponse(response);
  }
  
}
