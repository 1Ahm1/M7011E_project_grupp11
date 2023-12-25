export interface Book {
    id: number;
    name: String;
    author: String;
    description: String;
    image?: String;
    price: number;
    stock: number;
    year: String;
    language: String;
}

export interface Order {
    id: number;
    book: Book;
    quantity: number;
    selected: boolean;
}

export interface UserProfile {
    userId: number;
    email: String;
    phoneNumber: String;
    defaultLang: String;
    defaultRole: String;
    name: String;
    imageUrl: String;
}
export interface LoginData {
    accessToken: String;
    refreshToken: String;
    userProfile: UserProfile;
}

export interface RegisterData {
    pendingUserId: number;
}
