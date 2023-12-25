import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, map } from 'rxjs';
import { Book } from '../interfaces/entities';
import { BookService } from '../services/book.service';
import { CartService } from '../services/cart.service';
import { success, fail } from 'src/utils/general';
@Component({
  selector: 'app-book-details',
  templateUrl: './book-details.component.html'
})
export class BookDetailsComponent {

  quantity: number = 0;
  bookId: number = 0
  book: Book = {
    id: 0,
    name: '',
    author: '',
    description: '',
    image: 'https://d1csarkz8obe9u.cloudfront.net/posterpreviews/art-book-cover-design-template-34323b0f0734dccded21e0e3bebf004c_screen.jpg?ts=1637015198',
    price: 0,
    year: '',
    stock: 0,
    language: ''
  };
  bookService: BookService = inject(BookService);
  cartService: CartService = inject(CartService);
  stockOptions: number[] = [];
  constructor(private route: ActivatedRoute, private router: Router) {
    
  }
  goToHome() {
    this.router.navigate(['home/']);
  }
  async ngOnInit() {
    this.route.params.subscribe(s => {
      this.bookId = s['bookId'];
    })
    await this.getBookDetails(this.bookId)
    this.stockOptions = Array.from(Array(this.book.stock).keys());
  }
  async getBookDetails(bookId: number) {
    try
    {
      this.book = await this.bookService.getBookDetails(bookId);
    }
    catch(e) {
      console.log('error fetching book');
    }
  }
  async addToCart()
  {
    this.cartService.addToCart(Number(this.bookId), Number(this.quantity));
    success('Book added to cart successfully');
  }
}
