export interface LoginRequest {
    email: String;
    password: String;
}

export interface RegisterRequest {
    email: String;
    password: String;
    name: String;
    role: String;
}

export interface ValidateUserRequest {
    pending_user_id: number;
    email: String;
    validation_code: number;
    role: String;
}

export interface RefreshTokenRequest {
    refresh_token: String;
    role: String;
}

export interface CreateOrderRequest {
    book_id: number;
    quantity: number;
}

export interface UpdateProfileRequest {
    name: String;
}

export interface CreateBookRequest {
    name: String;
    author: String;
    description: String;
    stock: number;
    price: number;
    year: String;
    language: String;
}

export interface UpdateBookRequest
{
    book_id: number;
    name: String;
    author: String;
    description: String;
    stock: number;
    price: number;
    year: String;
    language: String;
}