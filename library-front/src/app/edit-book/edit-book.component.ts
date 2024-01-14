import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookService } from '../services/book.service';
import { success, fail } from 'src/utils/general';
import { Book } from '../interfaces/entities';

@Component({
  selector: 'app-edit-book',
  templateUrl: './edit-book.component.html'
})
export class EditBookComponent {
  bookId: number = 0;
  name: String = '';
  author: String = '';
  description: String = '';
  year: String = '';
  price: number = 0;
  language: String = '';
  stock: number = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private bookService: BookService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(s => {
      this.bookId = s['bookId'];
    })
    this.loadBook();
  }

  async loadBook() {
    const book: Book = await this.bookService.getBookDetails(this.bookId);
    this.bookId = book.id;
    this.name = book.name;
    this.author = book.author;
    this.description = book.description;
    this.year = book.year;
    this.price = book.price;
    this.language = book.language;
    this.stock = book.stock;
  }

  async updateBook() {
    try
    {
      await this.bookService.updateBook(this.bookId, this.name, this.author, this.stock, this.description, this.price, this.year, this.language);
      success('Book updated successfully');
      this.router.navigate(['manager/home'])
    }
    catch(e)
    {
      fail('Error creating the book');
      console.log('error adding book');
    }
  }
}
