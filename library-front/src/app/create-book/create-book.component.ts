import { Component, inject } from '@angular/core';
import { BookService } from '../services/book.service';
import { success, fail } from 'src/utils/general';
@Component({
  selector: 'app-create-book',
  templateUrl: './create-book.component.html'
})
export class CreateBookComponent {
  constructor() {
  }

  name: String = '';
  author: String = '';
  description: String = '';
  year: String = '';
  price: number = 0;
  language: String = '';
  stock: number = 0;

  private bookService: BookService = inject(BookService);
  async addBook() {
    try
    {
      await this.bookService.createBook(this.name, this.author, this.stock, this.description, this.price, this.year, this.language);
      this.name = '';
      this.author = '';
      this.description = '';
      this.year = '';
      this.price = 0;
      this.language = '';
      this.stock = 0;
      success('Book added successfully');

    }
    catch(e)
    {
      fail('Error creating the book');
      console.log('error adding book');
    }
  }
}
