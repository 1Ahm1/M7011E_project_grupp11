interface UserProfile {
    user_id: number;
    email: String;
    phone_number: String;
    default_lang: String;
    name: String;
    image_url: String;
}

export interface LoginResponse {
    access_token: String;
    refresh_token: String;
    user_profile: UserProfile;
}

export interface RegisterResponse {
    pending_user_id: number;
}

export interface BookListResponse {
    book_id: number;
    name: String;
    author: String;
    image: String;
    price: number;
    year: String;
    language: String;
}

export interface OrderListResponse {
    order_id: number,
    book_id: number,
    quantity: number
}

export interface GetProfileResponse {
    user_id: number;
    email: String;
    phone_number?: String;
    default_lang: String;
    default_role: String;
    name: String;
    image_url?: String;
}