import { Component, inject } from '@angular/core';
import { BookService } from '../services/book.service';
import { Book } from '../interfaces/entities';
import { Router } from '@angular/router';

@Component({
  selector: 'app-book-list',
  templateUrl: './book-list.component.html'
})
export class BookListComponent {
  bookList: Book[][] = [[]]
  bookService: BookService = inject(BookService)
  columns = 4
  search: String = '';
  constructor(private router: Router) {
    this.getBookList()
  }
  goToHome() {
    this.router.navigate(['home/']);
  }
  async updateFilter() {
    this.bookList = [[]];
    if(this.search == '')
    {
      await this.getBookList()
    }
    else
    {
      let books = await this.bookService.getBooks();
      books = books.filter((book) =>
        book.name.toLowerCase().includes(this.search.toLowerCase())
      );
        for(let i = 0; i < books.length; i += this.columns) {
          this.bookList.push(books.slice(i, i + this.columns))
        }
    }
      
  }
  async getBookList() {
    try
    {
      const books = await this.bookService.getBooks();
      for(let i = 0; i < books.length; i += this.columns) {
        this.bookList.push(books.slice(i, i + this.columns))
      }
    }
    catch(e) {
      console.log('error fetching books');
    }
  }
}
