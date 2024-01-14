import { Component } from '@angular/core';
import { BookService } from '../services/book.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-manager-book-list',
  templateUrl: './manager-book-list.component.html'
})
export class ManagerBookListComponent {
  books: any[] = []; // Replace 'any[]' with the actual type of your book objects

  constructor(private bookService: BookService, private router: Router) {}

  ngOnInit() {
    this.loadBooks();
  }

  async loadBooks() {
    this.books = await this.bookService.getBooks();
  }

  async deleteBook(bookId: number) {
    await this.bookService.deleteBook(bookId);
    window.location.reload();
  }

  addBook() {
    this.router.navigate(['manager/create']);
  }
}
